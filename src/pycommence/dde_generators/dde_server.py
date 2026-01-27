from functools import wraps

import pythoncom
import win32ui  # noqa
import dde
from loguru import logger

from pycommence.dde_generators.dde_msg import DDEMessage
from pycommence.exceptions import PyCommenceDDEError
from pycommence.meta.pycmc_fields import DELIM
from pycommence.wrapper.conversation_wrapper import DDEKind, DDETopic


def parse_com_error_code(args: tuple) -> int:
    long_code, basic_msg, code_tup, sometype = args
    code = code_tup[0]
    return code


def dde_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pythoncom.error as e:
            code = parse_com_error_code(e.args)
            raise PyCommenceDDEError(args[1], code) from e
        except dde.error as e:
            raise PyCommenceDDEError(args[1], -1, str(e)) from e

    return wrapper


class DDEServer:
    def __init__(self, topic: DDETopic = DDETopic.GET, application='Commence'):
        self._topic = topic
        self.server = None
        self.connected = None
        self.conversation = None
        self.application = application

    def establish_conversation(self):
        if self.conversation is not None:
            return
        self.conversation = dde.CreateConversation(self.server)

    @dde_error_handler
    def connect(self, topic: DDETopic):
        if self.connected == topic:
            return self.conversation
        self.conversation.ConnectTo(self.application, topic)
        self.connected = topic
        return self.conversation

    @dde_error_handler
    def __enter__(self):
        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        self.server = dde.CreateServer()
        self.server.Create('pycommence_dde_client')
        self.conversation = dde.CreateConversation(self.server)
        self.connect(self._topic)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pythoncom.CoUninitialize()
        self.server.Destroy()

    def send_message(self, msg: DDEMessage):
        self.connect(msg.topic)
        cmd = msg.commence_format
        logger.debug(f'Sending DDE message: {cmd}')
        if msg.kind == DDEKind.REQUEST:
            res = self._send_request(cmd)
        elif msg.kind == DDEKind.EXECUTE:
            res = self._send_execute(cmd)
        else:
            raise ValueError(f'Unknown DDE kind: {msg.kind}')
        if isinstance(res, str) and DELIM in res:
            res = res.split(DELIM)
        if not isinstance(res, list):
            logger.warning(f'Received DDE response not list: {res}\n' * 10)
        return res

    @dde_error_handler
    def _send_request(self, cmd: str) -> str | bool:
        return self.conversation.Request(cmd)

    @dde_error_handler
    def _send_execute(self, cmd: str) -> str | bool:
        return self.conversation.Exec(cmd)
