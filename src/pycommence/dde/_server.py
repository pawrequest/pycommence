import threading
from functools import wraps
from typing import Callable, Sequence

import pythoncom
import win32ui  # noqa
import dde
from loguru import logger

from . import msgs
from .types import DDEKind, DDEMessage, DDETopic
from pycommence.core.exceptions import PyCommenceDDEError
from pycommence.core.fields import DELIM
from pycommence.com.context import com_multithreaded_context


def dde_handler(func: Callable):
    """ Decorator to handle lock and DDE errors for DDEServer methods. First Arg must be DDEServer instance. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(args[0], DDEServer):
            raise ValueError('DDE Error handler - requires DDEServer as first argument')
        self: DDEServer = args[0]
        cmd = str(args[1]) if len(args) > 1 else func.__name__
        try:
            res = func(*args, **kwargs)
            raise_for_bad_dde(cmd, res)
            return res

        except pythoncom.error as e:
            long_code, basic_msg, code_tup, sometype, rest = e.args
            code = code_tup[0]
            raise PyCommenceDDEError(cmd, code) from e

        except dde.error as e:
            try:
                code = self.last_error()
                raise PyCommenceDDEError(cmd, code) from e
            except Exception as e2:
                if isinstance(e2, PyCommenceDDEError):
                    raise e2 from e
                e.add_note('Additionally, failed to get DDE error code from server.')
                raise e

    return wrapper


def raise_for_bad_dde(cmd: str, res):
    if isinstance(res, str) and res == '(Active item not found)':
        raise PyCommenceDDEError(cmd=cmd, code=666, msg='Active item not found')


class DDEOptions:
    strip_strs: bool = False
    split_str_lists: bool = True
    max_cmd_len = 256  # undocumented limit in Commence DDE for command length
    fields_chunk = 12
    client_name: str = 'pycommence_dde_client'
    application_name: str = 'Commence'


class DDEServer:
    def __init__(self, options: DDEOptions = DDEOptions()):
        self.options = options
        self._server = None
        self.connected = None
        self._conversation = None
        self._lock = threading.RLock()
        self._com_context = None

    @property
    def conversation(self):
        if self._conversation is None:
            self._create_conversation()
        return self._conversation

    def __enter__(self):
        self._com_context = com_multithreaded_context()
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

    def send_message(self, msg: DDEMessage):
        self._connect_topic(msg.topic)
        method = self._send_execute if msg.kind == DDEKind.EXECUTE else self._send_request
        res = method(msg)
        return self._handle_response(res)

    def _handle_response(self, res: str | bool) -> str | list[str] | bool:
        if isinstance(res, str):
            if self.options.strip_strs:
                res = res.strip()
            if DELIM in res and self.options.split_str_lists:
                res = res.split(DELIM)
        lentext = str(len(res)) if isinstance(res, Sequence) else 'N/A'
        logger.debug(f'Received DDE response ({type(res).__name__}, len={lentext}): {res}')
        return res if res else EMPTY

    @dde_handler
    def _send_request(self, cmd: str | DDEMessage) -> str | bool:
        with self._lock:
            logger.debug(f'Sending DDE request: {cmd}')
            return self.conversation.Request(str(cmd))

    @dde_handler
    def _send_execute(self, cmd: str | DDEMessage) -> str | bool:
        with self._lock:
            logger.debug(f'Sending DDE execute: {cmd}')
            return self.conversation.Exec(str(cmd))

    def last_error(self) -> int:
        # if not self.connected == DDETopic.SYSTEM:
        #     self._connect_topic(DDETopic.SYSTEM)
        # res = self._send_request('GetLastError')
        msg = msgs.request.get_last_error()
        res = self.send_message(msg)
        try:
            return int(res)
        except (ValueError, TypeError):
            return res

    def _last_error_no_lock(self) -> int:
        try:
            logger.debug('Getting last DDE error without lock')
            if self.connected != DDETopic.SYSTEM:
                self.conversation.ConnectTo(self.options.application_name, DDETopic.SYSTEM.value)
            res = int(self.conversation.Request('GetLastError'))
            return res
        except Exception as e:
            logger.error('Failed to get last DDE error without lock')
            raise PyCommenceDDEError(cmd='GetLastError', code=-1, msg='Failed to get last DDE error') from e

    @dde_handler
    def _create_server(self):
        with self._lock:
            self._server = dde.CreateServer()
            self._server.Create(self.options.client_name)
        assert self._server is not None, "Failed to create DDE server"

    @dde_handler
    def _create_conversation(self):
        with self._lock:
            self._conversation = dde.CreateConversation(self._server)

    @dde_handler
    def _connect_topic(self, topic: DDETopic):
        if self.connected == topic:
            return
        with self._lock:
            self.conversation.ConnectTo(self.options.application_name, topic.value)
        self.connected = topic


EMPTY = 'empty'
