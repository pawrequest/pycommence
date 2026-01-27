from __future__ import annotations

from enum import StrEnum

import pywintypes
from loguru import logger

from pycommence.exceptions import PyCommenceDDEError
from pycommence.meta.pycmc_fields import DELIM
from pycommence.wrapper._icommence import ICommenceConversation


class DDETopic(StrEnum):
    VIEW = 'ViewData'
    GET = 'GetData'
    SYSTEM = 'System'


class DDEKind(StrEnum):
    REQUEST = 'request'
    EXECUTE = 'execute'


def parse_com_error_code(args: tuple):
    long_code, basic_msg, code_tup, sometype = args
    code = code_tup[0]
    return code


class ConversationAPI:
    """Thin Wrapper on Commence's Conversation object using DDE."""

    def __init__(self, cmc_conversation: ICommenceConversation):
        self._conv_wrapper = cmc_conversation

    def send_dde(self, cmd: str, kind: DDEKind = DDEKind.REQUEST) -> str | bool:
        try:
            if kind == DDEKind.EXECUTE:
                return self._conv_wrapper.Execute(cmd)
            elif kind == DDEKind.REQUEST:
                return self._conv_wrapper.Request(cmd)
            else:
                raise ValueError(f'Unknown DDE kind: {kind}')
        except pywintypes.com_error as e:
            code = parse_com_error_code(e.args)
            raise PyCommenceDDEError(cmd, code) from e


class ConversationManager:
    """Manages multiple DDE conversations."""

    def __init__(self, *topics: DDETopic):
        self._conversations: dict[DDETopic, ConversationAPI] = {}
        for topic in topics:
            self._conversations[topic] = None

    def add_conversation(self, topic: DDETopic, conversation: ConversationAPI):
        self._conversations[topic] = conversation

    def get_conversation(self, topic: DDETopic) -> ConversationAPI | None:
        return self._conversations.get(topic)

    def send_dde(self, cmd: str, topic: DDETopic = DDETopic.VIEW, kind: DDEKind = DDEKind.REQUEST):
        logger.debug(f'Sending DDE: {topic}:{kind}: {cmd}')
        conv = self.get_conversation(topic)
        if conv is None:
            raise ValueError(f'No conversation established for topic: {topic}')
        res = conv.send_dde(cmd, kind)
        if isinstance(res, str) and DELIM in res:
            res = res.split(DELIM)
        logger.debug(f'Received DDE: {topic}:{kind}:type{type(res)} len{len(res)}')
        return res
