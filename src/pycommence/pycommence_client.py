import threading
from typing import cast

from win32com.client import Dispatch
from loguru import logger
from win32com.universal import com_error

from pycommence.cursor import CursorAPI
from pycommence.threads import com_context
from pycommence.core.exceptions import PyCommenceServerError
from pycommence.dde import DDEMessageBase, DDETopic, msgs
from pycommence.dde.dde_errors import dde_error_handler
from pycommence.dde.types import EMPTY
from pycommence.conversation import ConversationAPI
from pycommence.icommence.db import ICommenceDB
from pycommence.pycommence_options import Options, get_options
from pycommence.icommence.const import CursorType, OptionFlag
from pycommence.icommence.cursor_wrapper import CursorWrapper


class _PyCommenceClientConnector:
    def __init__(self, options: Options = get_options()):
        self.options: Options = options
        self._lock = threading.RLock()
        self._com_context = None
        self._cmc_app: ICommenceDB | None = None
        self._conversations: dict[DDETopic, ConversationAPI] = {}
        self.cursors: dict[str, CursorAPI] = {}

    def __enter__(self):
        self._com_context = com_context()
        self._com_context.__enter__()
        self._init_in_context()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            logger.debug('Exiting PyCommenceClient context')
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

    def _connect_app(self) -> ICommenceDB:
        with self._lock:
            res1 = Dispatch(self.options.application_db_name)
            return cast(ICommenceDB, cast(object, res1))

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
            raise ValueError(f'Conversation topic must be specified if multiple or zero conversations exist.{self._conversations=}')
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
    def cursor(self, name: str) -> CursorAPI:
        name = name or self._sole_cursor_name()
        return self.cursors.get(name) or self._create_cursor(name)

    def refresh_cursor(self, csrname: str = None) -> CursorAPI:
        """Reset an existing cursor with same name and mode."""
        csrname = csrname or self._sole_cursor_name()
        csr = self.cursors[csrname]
        self.cursors[csrname] = self._create_cursor(csrname, csr.mode)
        return self.cursors[csrname]

    def _create_cursor(
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


class PyCommenceClient(_PyCommenceClientConnector):
    @dde_error_handler
    def send_dde_message(self, msg: DDEMessageBase) -> str | list[str] | bool:
        conv = self.conversation(msg.topic)
        return conv.send_message(msg)

    def item_read_dde(self, category, name, fields: list[str] = None, topic: DDETopic = DDETopic.GET) -> dict[str, str]:
        item_dict = {}
        field_names = fields if fields else self.conversation(topic).category_field_names(category)
        master_msg = msgs.get.fields(category=category, item=name, fields=field_names, delim=self.options.delim)

        if len(str(master_msg)) < self.options.max_cmd_len:
            res = self.send_dde_message(master_msg)
            for attr, value in zip(field_names, res):
                item_dict[attr] = value
        else:
            for start in range(0, len(field_names), self.options.fields_chunk):
                fields_chunk = field_names[start:start + self.options.fields_chunk]
                chunk_msg = msgs.get.fields(
                    category=category,
                    item=name,
                    fields=fields_chunk,
                    delim=self.options.delim
                )
                chunk_res = self.send_dde_message(chunk_msg)
                for attr, value in zip(fields_chunk, chunk_res):
                    item_dict[attr] = value
        assert len(item_dict) == len(field_names)
        return item_dict

    def item_add_dde(self, category, item_name: str, topic: DDETopic) -> bool:
        msg = msgs.execute.add_item(category, item_name, topic)
        res = self.send_dde_message(msg)
        return res

    def item_delete_dde(self, category, item_name: str, topic: DDETopic) -> bool:
        msg = msgs.execute.delete_item(category, item_name, topic)
        res = self.send_dde_message(msg)
        return res

    def item_edit_dde(
            self,
            category,
            item_name: str,
            field_updates: dict[str, str],
            topic: DDETopic = DDETopic.GET
    ) -> bool:
        for field_name, field_value in field_updates.items():
            msg = msgs.execute.edit_item(category, item_name, field_name, field_value, topic)
            res = self.send_dde_message(msg)
            assert res is True
        return True

