# from __future__ import annotations
#
# import pywintypes
# from loguru import logger
#
# from pycommence.dde import DDEKind, DDEMessageBase
# from pycommence.dde.dde_errors import PyCmcDDEError, commence_pycom_error_code
# from pycommence.icommence.conversation import ICommenceConversation
# from pycommence.pycommence_options import get_options
#
# DELIM = get_options().delim
#
#
# def parse_com_error_code(args: tuple):
#     long_code, basic_msg, code_tup, sometype = args
#     code = code_tup[0]
#     return code
#
#
# class ConversationAPI:
#     """Thin Wrapper on Commence's Conversation object using DDE."""
#
#     def __init__(self, cmc_conversation: ICommenceConversation):
#         self._conv = cmc_conversation
#
#     def send_dde(self, cmd: str, kind: DDEKind = DDEKind.REQUEST) -> str | bool:
#         try:
#             if kind == DDEKind.EXECUTE:
#                 return self._conv.Execute(cmd)
#             elif kind == DDEKind.REQUEST:
#                 return self._conv.Request(cmd)
#             else:
#                 raise ValueError(f'Unknown DDE kind: {kind}')
#         except pywintypes.com_error as e:
#             code = commence_pycom_error_code(e)
#             raise PyCmcDDEError(cmd, code) from e
#
#     def send_dde_msg(self, msg: DDEMessageBase) -> str | bool:
#         logger.debug(f'Sending DDE message: {msg}')
#         try:
#             if msg.kind == DDEKind.EXECUTE:
#                 res = self._conv.Execute(str(msg))
#             elif msg.kind == DDEKind.REQUEST:
#                 res = self._conv.Request(str(msg))
#             else:
#                 raise ValueError(f'Unknown DDE kind: {msg.kind}')
#         except pywintypes.com_error as e:
#             code = commence_pycom_error_code(e)
#             raise PyCmcDDEError(str(msg), code) from e
#         if isinstance(res, str) and DELIM in res:
#             res = res.split(DELIM)
#         return res
import threading
from collections.abc import Sequence

from loguru import logger

from pycommence.core.exceptions import PyCommenceServerError
from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition
from pycommence.core.filters import CmcFilter, ConditionType, FieldFilter
from pycommence.core.meta import FetchMode, generate_table_pydantic_model, get_table_type
from pycommence.dde import DDEKind, DDEMessageBase, msgs
from pycommence.dde.dde_errors import PyCmcDDEStatusError, dde_error_handler
from pycommence.dde.types import EMPTY
from pycommence.icommence import ICommenceConversation
from pycommence.pycommence_options import Options, get_options


class ConversationAPI:
    def __init__(self, conv: ICommenceConversation, options: Options = get_options()):
        self._lock = threading.RLock()
        self.conv = conv
        self.options = options

    # @dde_error_handler
    def _send_message_raw(self, msg: DDEMessageBase) -> str | bool:
        logger.debug(f'Sending DDE message: {msg}')
        with self._lock:
            res = self.conv.Execute(str(msg)) if msg.kind == DDEKind.EXECUTE else self.conv.Request(str(msg))
        logger.debug(f'Received raw DDE response ({type(res).__name__}): {res}')
        if not isinstance(res, str | bool):
            raise PyCommenceServerError(f'Unexpected response type from DDE: {type(res).__name__}')
        return res

    def send_message(self, msg: DDEMessageBase) -> str | list[str] | bool:
        res = self._send_message_raw(msg)
        return self._handle_dde(res)

    def _handle_dde(self, res: str | bool) -> str | list[str] | bool:
        if isinstance(res, str):
            if self.options.split_str_lists and self.options.delim in res:
                res = res.split(self.options.delim)
        lentext = str(len(res)) if isinstance(res, Sequence) else 'N/A'
        logger.debug(f'Processed DDE response ({type(res).__name__}, len={lentext}): {res}')
        return res if res else EMPTY

    def status_check(self):
        try:
            assert self.send_message(msgs.system.status()) == 'Ready'
        except AssertionError:
            raise PyCmcDDEStatusError

    def db_name_and_path(self):
        """Returns the current database as (name, path)"""
        return self.send_message(DDEMessageBase(func_name='GetDatabase', params=[self.options.delim]))

    # CATEGORY
    def category_field_names(self, category: str):
        msg = msgs.get.field_names(category)
        field_names = self.send_message(msg)
        return field_names

    def category_field_definitions(self, category: str, fields: list[str] = None) -> CmcDefsDict:
        """Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
        fields_definitions = CmcDefsDict()
        fields = fields or self.category_field_names(category)
        for field_name in fields:
            field_definition_res = self._field_defintion_raw(category, field_name)
            field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
            fields_definitions[field_name] = field_definition
        return fields_definitions

    # VIEW
    def view_reset(self, category: str):
        self.send_message(msgs.view.category(category))

    def view_filter(self, filter_: CmcFilter, slot=1) -> int:
        # cmd = str(filter_.view_filter_str(slot))
        msg = msgs.view.filter_(slot, *filter_.get_params)
        return self.send_message(msg)

    def view_filter_by_field(self, field, value: str, slot=1, condition: ConditionType = ConditionType.CONTAIN) -> int:
        filter_ = FieldFilter(column=field, value=value, condition=condition)
        return self.view_filter(filter_, slot=slot)

    # ROW / FIELD
    def row_count(self):
        return int(self.send_message(msgs.view.item_count()))

    def _field_defintion_raw(self, category: str, field_name: str) -> bool | str | list[str]:
        msg = msgs.get.field_definition(category, field_name)
        field_definition = self.send_message(msg)
        return field_definition

    def field_definition(self, category: str, field_name: str) -> CmcFieldDefinition:
        field_definition_res = self._field_defintion_raw(category, field_name)
        field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
        return field_definition


def get_or_create_table_type(
    self: ConversationAPI, category: str, mode: FetchMode = 'all'
) -> type['CommenceTableGenerated'] | type['CommenceTable']:
    table_type = get_table_type(category, mode=mode, missing='ignore')
    if not table_type:
        field_defs = self.category_field_definitions(category)
        table_type = generate_table_pydantic_model(category, category, field_defs)
    return table_type
