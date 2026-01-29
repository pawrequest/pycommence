from __future__ import annotations

import pywintypes
from loguru import logger

from pycommence.core.fields import DELIM
from pycommence.dde import DDEKind, DDEMessageBase
from pycommence.dde.dde_errors import commence_pycom_error_code, PyCmcDDEError
from pycommence.wrapper._icommence import ICommenceConversation


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
            code = commence_pycom_error_code(e)
            raise PyCmcDDEError(cmd, code) from e

    def send_dde_msg(self, msg: DDEMessageBase) -> str | bool:
        logger.debug(f'Sending DDE message: {msg}')
        try:
            if msg.kind == DDEKind.EXECUTE:
                res = self._conv_wrapper.Execute(str(msg))
            elif msg.kind == DDEKind.REQUEST:
                res = self._conv_wrapper.Request(str(msg))
            else:
                raise ValueError(f'Unknown DDE kind: {msg.kind}')
        except pywintypes.com_error as e:
            code = commence_pycom_error_code(e)
            raise PyCmcDDEError(str(msg), code) from e
        if isinstance(res, str) and DELIM in res:
            res = res.split(DELIM)
        return res
