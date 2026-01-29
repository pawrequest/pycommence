from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition, DELIM
from pycommence.core.filters import CmcFilter, ConditionType, FieldFilter
from pycommence.core.meta import generate_table_pydantic_model, get_table_type
from . import msgs
from .types import DDEMessage, DDETopic
from ._server import DDEServer, EMPTY


class PyCmcDDEServer(DDEServer):
    def db_name(self) -> tuple[str, str]:
        """ Returns the current database as (name, path) """
        return self.send_message(DDEMessage(func_name='GetDatabase', params=[DELIM]))

    def reset_view(self, category: str, topic: DDETopic = DDETopic.GET):
        self.send_message(msgs.view.view_category(category, topic=topic))

    def filter_view(self, filter_: CmcFilter, slot=1) -> int:
        return self._send_request(filter_.view_filter_str(slot))

    def filter_view_by_fields(self, field, value: str, slot=1, condition: ConditionType = ConditionType.CONTAIN) -> int:
        filter_ = FieldFilter(column=field, value=value, condition=condition)
        return self.filter_view(filter_, slot=slot)

    def row_count(self):
        return int(self.send_message(msgs.view.view_item_count()))

    def item_read(self, category, name, fields: list[str] = None) -> dict[str, str]:
        item_dict = {}
        field_names = fields if fields else self.category_field_names(category)

        master_msg = msgs.request.get_fields(category=category, item=name, fields=field_names, delim=DELIM)

        if len(str(master_msg)) < self.options.max_cmd_len:
            res = self.send_message(master_msg)
            for attr, value in zip(field_names, res):
                item_dict[attr] = value
        else:
            for start in range(0, len(field_names), self.options.fields_chunk):
                fields_chunk = field_names[start:start + self.options.fields_chunk]
                chunk_msg = msgs.request.get_fields(category=category, item=name, fields=fields_chunk, delim=DELIM)
                chunk_res = self.send_message(chunk_msg)
                for attr, value in zip(fields_chunk, chunk_res):
                    item_dict[attr] = value
        assert len(item_dict) == len(field_names)
        return item_dict

    def category_field_names(self, category: str) -> bool | str | list[str]:
        msg = msgs.request.get_field_names(category)
        field_names = self.send_message(msg)
        return field_names

    def _field_defintion_raw(self, category: str, field_name: str) -> bool | str | list[str]:
        msg = msgs.request.get_field_definition(category, field_name)
        field_definition = self.send_message(msg)
        return field_definition

    def field_definition(self, category: str, field_name: str) -> CmcFieldDefinition:
        field_definition_res = self._field_defintion_raw(category, field_name)
        field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
        return field_definition

    def fields_definition_dict(self, category: str, fields: list[str] = None) -> CmcDefsDict:
        """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
        fields_definitions = CmcDefsDict()
        fields = fields or self.category_field_names(category)
        for field_name in fields:
            field_definition_res = self._field_defintion_raw(category, field_name)
            field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
            fields_definitions[field_name] = field_definition
        return fields_definitions

    def item_add(self, category, item_name: str, topic: DDETopic = DDETopic.VIEW) -> bool:
        assert self.send_message(msgs.execute.execute_add_item(category, item_name, topic=topic)) == EMPTY
        return True

    def item_delete(self, category, item_name: str) -> bool:
        assert self.send_message(msgs.execute.execute_delete_item(category, item_name)) == EMPTY
        return True

    def item_edit(
            self,
            category,
            item_name: str,
            field_updates: dict[str, str],
            topic: DDETopic = DDETopic.GET
    ) -> bool:
        for field_name, field_value in field_updates.items():
            msg = msgs.execute.execute_edit_item(category, item_name, field_name, field_value)
            msg.topic = topic
            assert self.send_message(msg) == EMPTY
        return True


def get_or_create_table_type(self, category: str):
    table_type = get_table_type(category, 'all')
    if not table_type:
        field_defs = self.fields_definition_dict(category)
        table_type = generate_table_pydantic_model(category, category, field_defs)
    return table_type
