import threading
from typing import Sequence

import pythoncom
from loguru import logger
from win32.lib.pywintypes import IID
from win32com import client

from pycommence.core.exceptions import PyCommenceServerError
from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition
from pycommence.core.filters import CmcFilter, ConditionType, FieldFilter
from pycommence.core.meta import generate_table_pydantic_model, get_table_type
from pycommence.dde import DDEKind, DDEMessageBase, DDETopic, msgs
from pycommence.dde.dde_errors import PyCmcDDEStatusError, dde_error_handler
from pycommence.dde.types import EMPTY
from pycommence.pycommence_options import Options, get_options

# from win32com.client import DispatchBaseClass

DispatchBaseClass = client.CDispatch
from pycommence.icommence.const import LCID


class ICommenceConversation(DispatchBaseClass):
    CLSID = IID('{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}')
    coclass_clsid = None

    def Execute(self, pszCommand):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((8, 1),), pszCommand)

    def Request(self, pszCommand):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((8, 1),), pszCommand)

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        'Return a Python iterator for this object'
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class ConversationAPI:
    def __init__(self, conv: ICommenceConversation, options: Options = get_options()):
        self._lock = threading.RLock()
        self.conv = conv
        self.options = options

    @dde_error_handler
    def _send_message_raw(self, msg: DDEMessageBase) -> str | bool:
        logger.debug(f'Sending DDE message: {msg}')
        with self._lock:
            res = self.conv.Execute(str(msg)) if msg.kind == DDEKind.EXECUTE else self.conv.Request(str(msg))
        logger.debug(f'Received DDE response ({type(res).__name__}): {res}')
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
        logger.debug(f'Received DDE response ({type(res).__name__}, len={lentext}): {res}')
        return res if res else EMPTY

    def status_check(self):
        try:
            assert self.send_message(msgs.system.status()) == 'Ready'
        except AssertionError as e:
            raise PyCmcDDEStatusError

    def db_name(self):
        """ Returns the current database as (name, path) """
        return self.send_message(DDEMessageBase(func_name='GetDatabase', params=[self.options.delim]))

    # CATEGORY
    def category_field_names(self, category: str):
        msg = msgs.get.field_names(category)
        field_names = self.send_message(msg)
        return field_names

    def category_field_definitions(self, category: str, fields: list[str] = None) -> CmcDefsDict:
        """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
        fields_definitions = CmcDefsDict()
        fields = fields or self.category_field_names(category)
        for field_name in fields:
            field_definition_res = self._field_defintion_raw(category, field_name)
            field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
            fields_definitions[field_name] = field_definition
        return fields_definitions

    # ITEM
    # def item_read(self, category, name, fields: list[str] = None) -> dict[str, str]:
    #     item_dict = {}
    #     field_names = fields if fields else self.category_field_names(category)
    #     master_msg = msgs.get.fields(category=category, item=name, fields=field_names, delim=self.options.delim)
    #
    #     if len(str(master_msg)) < self.options.max_cmd_len:
    #         res = self.send_message(master_msg)
    #         for attr, value in zip(field_names, res):
    #             item_dict[attr] = value
    #     else:
    #         for start in range(0, len(field_names), self.options.fields_chunk):
    #             fields_chunk = field_names[start:start + self.options.fields_chunk]
    #             chunk_msg = msgs.get.fields(
    #                 category=category,
    #                 item=name,
    #                 fields=fields_chunk,
    #                 delim=self.options.delim
    #             )
    #             chunk_res = self.send_message(chunk_msg)
    #             for attr, value in zip(fields_chunk, chunk_res):
    #                 item_dict[attr] = value
    #     assert len(item_dict) == len(field_names)
    #     return item_dict

    # def item_add(self, category, item_name: str, topic: DDETopic) -> bool:
    #     msg = msgs.execute.add_item(category, item_name, topic)
    #     res = self.send_message(msg)
    #     return res

    # def item_delete(self, category, item_name: str, topic: DDETopic) -> bool:
    #     msg = msgs.execute.delete_item(category, item_name, topic)
    #     res = self.send_message(msg)
    #     return res

    # def item_edit(
    #         self,
    #         category,
    #         item_name: str,
    #         field_updates: dict[str, str],
    #         topic: DDETopic = DDETopic.GET
    # ) -> bool:
    #     for field_name, field_value in field_updates.items():
    #         msg = msgs.execute.edit_item(category, item_name, field_name, field_value, topic)
    #         assert self.send_message(msg) == EMPTY
    #     return True

    # VIEW
    def view_reset(self, category: str):
        self.send_message(msgs.view.category(category))

    def view_filter(self, filter_: CmcFilter, slot=1) -> int:
        # cmd = str(filter_.view_filter_str(slot))
        msg = msgs.view.filter_(slot, *filter_.get_params)
        return self.send_message(msg)

    def view_filter_by_field(
            self,
            field,
            value: str,
            slot=1,
            condition: ConditionType = ConditionType.CONTAIN
    ) -> int:
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


def get_or_create_table_type(self: ConversationAPI, category: str):
    table_type = get_table_type(category, 'all')
    if not table_type:
        field_defs = self.category_field_definitions(category)
        table_type = generate_table_pydantic_model(category, category, field_defs)
    return table_type
