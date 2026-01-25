from __future__ import annotations

from enum import StrEnum

import pywintypes

from pycommence.exceptions import PyCommenceDDEError
from pycommence.wrapper._icommence import ICommenceConversation


class DDETopic(StrEnum):
    VIEW_DATA = 'ViewData'
    GET_DATA = 'GetData'
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

    def send_dde(self, dde_command: str, kind: DDEKind = DDEKind.REQUEST) -> str | bool:
        try:
            if kind == DDEKind.EXECUTE:
                return self._conv_wrapper.Execute(dde_command)
            elif kind == DDEKind.REQUEST:
                return self._conv_wrapper.Request(dde_command)
            else:
                raise ValueError(f'Unknown DDE kind: {kind}')
        except pywintypes.com_error as e:
            code = parse_com_error_code(e.args)
            raise PyCommenceDDEError(dde_command, code) from e
