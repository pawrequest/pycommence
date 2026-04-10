import threading
from collections.abc import Callable
from typing import cast

from win32com.client import Dispatch
from win32com.universal import com_error

from pycommence.conversation import ConversationAPI
from pycommence.core.exceptions import PyCommenceServerError
from pycommence.core.row_data import RowData
from pycommence.cursor import CursorAPI
from pycommence.dde import DDEMessageBase, DDETopic, msgs
from pycommence.dde.dde_errors import dde_error_handler

# from pycommence.dde.dde_errors import dde_error_handler
from pycommence.icommence.const import CursorType, OptionFlag
from pycommence.icommence.cursor_wrapper import CursorWrapper
from pycommence.icommence.db import ICommenceDB
from pycommence.pycommence_options import Options, get_options
from pycommence.threads import com_context


class _PyCommenceClientConnector:
    def __init__(self, *csrname, options: Options = get_options()):
        self.options: Options = options
        self._lock = threading.RLock()
        self._com_context = None
        self._cmc_app: ICommenceDB | None = None
        self._conversations: dict[DDETopic, ConversationAPI] = {}
        self.cursors: dict[str, CursorAPI] = {}
        self._init_csrs: tuple[str] | None = csrname

    def __enter__(self, init_csr: str | None = None) -> '_PyCommenceClientConnector':
        self._com_context = com_context()
        self._com_context.__enter__()
        self._init_in_context()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            with self._lock:
                self._conversations.clear()
                self.cursors.clear()
                if self._cmc_app is not None:
                    self._cmc_app = None
        finally:
            if self._com_context:
                self._com_context.__exit__(exc_type, exc_val, exc_tb)

    def _init_in_context(self):
        if self._cmc_app is not None:
            return
        with self._lock:
            self._cmc_app = self._cmc_app or self._connect_app()
            self._create_conversation(DDETopic.GET)
            if self._init_csrs:
                for csrname in self._init_csrs:
                    self.create_cursor(csrname)

    def _connect_app(self) -> ICommenceDB:
        with self._lock:
            try:
                dispatch_ = Dispatch(self.options.application_db_name)
                return cast(ICommenceDB, cast(object, dispatch_))
            except Exception as e:
                raise PyCommenceServerError(f'Error connecting to Commence application: {e}')

    # CONVERSATION METHODS
    def conversation(self, topic: DDETopic = None) -> ConversationAPI:
        topic = topic or self._sole_conversation_topic()
        return self._conversations.get(topic) or self._create_conversation(topic)

    # def _handle_dde(self, res: str | bool) -> str | list[str] | bool:
    #     if isinstance(res, str):
    #         if self.options.split_str_lists and self.options.delim in res:
    #             res = res.split(self.options.delim)
    #     lentext = str(len(res)) if isinstance(res, Sequence) else 'N/A'
    #     logger.debug(f'Received DDE response ({type(res).__name__}, len={lentext}): {res}')
    #     return res if res else EMPTY

    def _sole_conversation_topic(self) -> DDETopic:
        if not len(self._conversations) == 1:
            raise ValueError(
                f'Conversation topic must be specified if multiple or zero conversations exist.{self._conversations=}'
            )
        return next(iter(self._conversations.keys()))

    def _create_conversation(self, topic: DDETopic) -> ConversationAPI:
        appname = self.options.application_name
        with self._lock:
            conv = self._cmc_app.GetConversation(appname, topic)
            conv_api = ConversationAPI(conv)
        if conv is None:
            raise PyCommenceServerError(f'Could not create conversation object for {appname}|{topic}')
        self._conversations[topic] = conv_api
        return conv_api

    # CURSOR METHODS
    def cursor(self, name: str | None = None) -> CursorAPI:
        name = name or self._sole_cursor_name()
        return self.cursors.get(name) or self.create_cursor(name)

    def refresh_cursor(self, csrname: str = None) -> CursorAPI:
        """Reset an existing cursor with same name and mode."""
        csrname = csrname or self._sole_cursor_name()
        csr = self.cursors[csrname]
        self.cursors[csrname] = self.create_cursor(csrname, csr.mode)
        return self.cursors[csrname]

    def create_cursor(
        self,
        name: str | None = None,
        mode: CursorType = CursorType.CATEGORY,
        pilot: bool = False,
        internet: bool = False,
    ) -> CursorAPI:
        if pilot and internet:
            raise ValueError('Only one of pilot or internet can be set')
        if mode in [CursorType.CATEGORY, CursorType.VIEW] and not name:
            raise ValueError(f'{mode.name} cursor mode requires name param to be set')

        flags = OptionFlag.NONE
        if pilot:
            flags |= OptionFlag.PILOT
        if internet:
            flags |= OptionFlag.INTERNET

        try:
            with self._lock:
                icsr = self._cmc_app.GetCursor(mode, name, flags)
                csr = CursorWrapper(icsr)
                csr_api = CursorAPI(csr, mode=mode, csrname=name or '')
        except com_error as e:
            raise PyCommenceServerError(f'Error creating cursor for {name} in {self.options.application_name}: {e}')
        self.cursors[name] = csr_api  # todo store by unique key
        return csr_api

    def _sole_cursor_name(self) -> str | None:
        if not len(self.cursors) == 1:
            raise ValueError('Cursor name must be specified if multiple or zero cursors exist')
        return next(iter(self.cursors.keys()))


class PyCommence(_PyCommenceClientConnector):
    # CURSOR CRUD
    def item_read_csr(self, *, csrname: str | None = None, row_id: str | None = None, pk: str | None = None) -> RowData:
        csr = self.cursor(csrname)
        return csr.read_row(row_id=row_id, pk=pk)

    # DDE CRUD
    @dde_error_handler
    def send_dde_message(self, msg: DDEMessageBase) -> str | list[str] | bool:
        conv = self.conversation(msg.topic)
        return conv.send_message(msg)

    def _chunked_dde_request(
        self,
        items: list[str],
        build_msg: Callable[[list[str]], DDEMessageBase],
    ) -> list[str]:
        """Send a DDE request, adaptively chunking *items* to stay within the command length limit.

        Args:
            items: The variable-length portion of the command (e.g. field names).
            build_msg: Callable that builds a :class:`DDEMessageBase` from a
                subset of *items*.

        Returns:
            Flat list of result values in the same order as *items*.
        """
        master_msg = build_msg(items)
        if len(str(master_msg)) < self.options.max_cmd_len:
            res = self.send_dde_message(master_msg)
            return res if isinstance(res, list) else [res]

        results: list[str] = []
        remaining = list(items)
        while remaining:
            chunk_size, chunk_msg = self._fit_chunk(remaining, build_msg)
            res = self.send_dde_message(chunk_msg)
            results.extend(res if isinstance(res, list) else [res])
            remaining = remaining[chunk_size:]
        return results

    def _fit_chunk(
        self,
        remaining: list[str],
        build_msg: Callable[[list[str]], DDEMessageBase],
    ) -> tuple[int, DDEMessageBase]:
        """Find the largest chunk from the front of *remaining* that fits within max_cmd_len."""
        for size in range(min(self.options.fields_chunk, len(remaining)), 0, -1):
            msg = build_msg(remaining[:size])
            if len(str(msg)) < self.options.max_cmd_len:
                return size, msg
        raise ValueError(
            f'Cannot fit DDE command within {self.options.max_cmd_len} chars even with a single item: "{remaining[0]}"'
        )

    def item_read_dde(self, category, name, fields: list[str] = None, topic: DDETopic = DDETopic.GET) -> dict[str, str]:
        field_names = fields if fields else self.conversation(topic).category_field_names(category)

        def build_msg(chunk: list[str]) -> DDEMessageBase:
            return msgs.get.fields(category=category, item=name, fields=chunk, delim=self.options.delim)

        results = self._chunked_dde_request(field_names, build_msg)
        assert len(results) == len(field_names)
        return dict(zip(field_names, results))

    def item_add_dde(self, category, item_name: str, topic: DDETopic) -> bool:
        msg = msgs.execute.add_item(category, item_name, topic)
        res = self.send_dde_message(msg)
        return res

    def item_delete_dde(self, category, item_name: str, topic: DDETopic) -> bool:
        msg = msgs.execute.delete_item(category, item_name, topic)
        res = self.send_dde_message(msg)
        return res

    def item_edit_dde(
        self, category, item_name: str, field_updates: dict[str, str], topic: DDETopic = DDETopic.GET
    ) -> bool:
        for field_name, field_value in field_updates.items():
            msg = msgs.execute.edit_item(category, item_name, field_name, field_value, topic)
            res = self.send_dde_message(msg)
            assert res is True
        return True
