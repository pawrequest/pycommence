from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition
from pycommence.core.filters import CmcFilter, ConditionType, FieldFilter
from pycommence.core.meta import generate_table_pydantic_model, get_table_type
from pycommence.dde import msgs
from pycommence.dde._server import DDEServer
from pycommence.dde.dde_errors import PyCmcDDEStatusError
from pycommence.dde.types import DDEMessageBase, DDETopic, EMPTY
from pycommence.pycommence_options import get_options

DELIM = get_options().delim


class PyCmcDDEServer(DDEServer):
    def __enter__(self):
        super().__enter__()
        self.status_check()
        return self

    def status_check(self):
        try:
            assert self.send_message(msgs.system.status()) == 'Ready'
        except AssertionError as e:
            raise PyCmcDDEStatusError

    def db_name(self) -> tuple[str, str]:
        """ Returns the current database as (name, path) """
        return self.send_message(DDEMessageBase(func_name='GetDatabase', params=[DELIM]))

    # CATEGORY
    def category_field_names(self, category: str) -> bool | str | list[str]:
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

    # VIEW
    def view_reset(self, category: str):
        self.send_message(msgs.view.category(category))

    def view_filter(self, filter_: CmcFilter, slot=1) -> int:
        return self._send_request(filter_.view_filter_str(slot))

    def view_filter_by_fields(self, field, value: str, slot=1, condition: ConditionType = ConditionType.CONTAIN) -> int:
        filter_ = FieldFilter(column=field, value=value, condition=condition)
        return self.view_filter(filter_, slot=slot)

    def row_count(self):
        return int(self.send_message(msgs.view.item_count()))

    def item_read(self, category, name, fields: list[str] = None) -> dict[str, str]:
        item_dict = {}
        field_names = fields if fields else self.category_field_names(category)

        master_msg = msgs.get.fields(category=category, item=name, fields=field_names, delim=DELIM)

        if len(str(master_msg)) < self.options.max_cmd_len:
            res = self.send_message(master_msg)
            for attr, value in zip(field_names, res):
                item_dict[attr] = value
        else:
            for start in range(0, len(field_names), self.options.fields_chunk):
                fields_chunk = field_names[start:start + self.options.fields_chunk]
                chunk_msg = msgs.get.fields(category=category, item=name, fields=fields_chunk, delim=DELIM)
                chunk_res = self.send_message(chunk_msg)
                for attr, value in zip(fields_chunk, chunk_res):
                    item_dict[attr] = value
        assert len(item_dict) == len(field_names)
        return item_dict

    def _field_defintion_raw(self, category: str, field_name: str) -> bool | str | list[str]:
        msg = msgs.get.field_definition(category, field_name)
        field_definition = self.send_message(msg)
        return field_definition

    def field_definition(self, category: str, field_name: str) -> CmcFieldDefinition:
        field_definition_res = self._field_defintion_raw(category, field_name)
        field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
        return field_definition

    def item_add(self, category, item_name: str, topic: DDETopic) -> bool:
        assert self.send_message(msgs.execute.add_item(category, item_name, topic)) == EMPTY
        return True

    def item_delete(self, category, item_name: str, topic: DDETopic) -> bool:
        assert self.send_message(msgs.execute.delete_item(category, item_name, topic)) == EMPTY
        return True

    def item_edit(
            self,
            category,
            item_name: str,
            field_updates: dict[str, str],
            topic: DDETopic = DDETopic.GET
    ) -> bool:
        for field_name, field_value in field_updates.items():
            msg = msgs.execute.edit_item(category, item_name, field_name, field_value, topic)
            assert self.send_message(msg) == EMPTY
        return True


def get_or_create_table_type(self: PyCmcDDEServer, category: str):
    table_type = get_table_type(category, 'all')
    if not table_type:
        field_defs = self.category_field_definitions(category)
        table_type = generate_table_pydantic_model(category, category, field_defs)
    return table_type
