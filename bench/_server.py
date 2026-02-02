import threading
from collections.abc import Sequence

import win32ui  # noqa before dde import to ensure proper initialization order
import dde as pywindde
from loguru import logger

from pycommence.dde import msgs
from pycommence.dde.types import DDEExecuteBase, DDEKind, DDEMessageBase, DDERequestBase, DDETopic, EMPTY
from pycommence.dde.dde_errors import PyCmcDDEError, PyCmcDDENoConnectionError, dde_error_handler
from pycommence.threads import com_context


class DDEOptions:
    strip_strs: bool = False
    split_str_lists: bool = True
    max_cmd_len = 256  # undocumented limit in Commence DDE for command length
    fields_chunk = 12
    client_name: str = 'pycommence_dde_client'
    application_name: str = 'Commence'
    delim: str = r'*&^%£$&^*'


class DDEServer:
    def __init__(self, options: DDEOptions = DDEOptions()):
        self.options = options
        self._server = None
        self.connected = None
        self._lock = threading.RLock()
        self._com_context = None
        self._conversation = None

    @property
    def conversation(self):
        if self._conversation is None:
            self._create_conversation()
        return self._conversation

    def __enter__(self):
        self._com_context = com_context()
        self._com_context.__enter__()
        self._create_server()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            logger.debug('Destroying DDE server...')
            self._server.Destroy()
        finally:
            if self._com_context:
                self._com_context.__exit__(exc_type, exc_val, exc_tb)

    def send_message(self, msg: DDEMessageBase):
        self._connect_topic(msg.topic)
        method = self._send_execute if msg.kind == DDEKind.EXECUTE else self._send_request
        res = method(msg)
        return self._handle_response(res)

    def _handle_response(self, res: str | bool) -> str | list[str] | bool:
        if isinstance(res, str):
            if self.options.strip_strs:
                res = res.strip()
            delim = self.options.delim
            if delim in res and self.options.split_str_lists:
                res = res.split(self.options.delim)
        lentext = str(len(res)) if isinstance(res, Sequence) else 'N/A'
        logger.debug(f'Received DDE response ({type(res).__name__}, len={lentext}): {res}')
        return res if res else EMPTY

    @dde_error_handler
    def _send_request(self, cmd: str | DDERequestBase) -> str | bool:
        with self._lock:
            logger.debug(f'Sending DDE request: {cmd}')
            return self.conversation.Request(str(cmd))

    @dde_error_handler
    def _send_execute(self, cmd: str | DDEExecuteBase) -> str | bool:
        with self._lock:
            logger.debug(f'Sending DDE execute: {cmd}')
            return self.conversation.Exec(str(cmd))

    def last_error(self) -> int:
        msg = msgs.get.last_error()
        res = self.send_message(msg)
        try:
            return int(res)
        except (ValueError, TypeError):
            return res

    def _last_error_no_handler(self) -> int:
        with self._lock:
            try:
                if self.connected != DDETopic.GET:
                    self.conversation.ConnectTo(self.options.application_name, DDETopic.GET.value)
                res = int(self.conversation.Request('GetLastError'))
                return res
            except Exception as e:
                if e.args[0] == 'ConnectTo failed':
                    raise PyCmcDDENoConnectionError
                logger.error('Failed to get last DDE error')
                raise PyCmcDDEError(cmd='GetLastError', code=-1, msg='Failed to get last DDE error') from e

    @dde_error_handler
    def _create_server(self):
        with self._lock:
            self._server = pywindde.CreateServer()
            self._server.Create(self.options.client_name)
        assert self._server is not None, 'Failed to create DDE server'

    @dde_error_handler
    def _create_conversation(self):
        with self._lock:
            self._conversation = pywindde.CreateConversation(self._server)

    @dde_error_handler
    def _connect_topic(self, topic: DDETopic):
        if self.connected == topic:
            return
        with self._lock:
            self.conversation.ConnectTo(self.options.application_name, topic.value)
        self.connected = topic


