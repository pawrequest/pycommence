from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition, DELIM
from pycommence.dde._server import DDEServer
from pycommence.dde.msgs.get import get_field_names, get_fields, get_field_definition

MAX_CMD_LEN = 256  # undocumented limit in Commence DDE for command length
MAX_FIELDS_CHUNK = 15


def fetch_field_names(category: str, server: DDEServer) -> bool | str | list[str]:
    msg = get_field_names(category)
    field_names = server.send_message(msg)
    return field_names


def _fetch_field_defintion_raw(category: str, field_name: str, server) -> bool | str | list[str]:
    msg = get_field_definition(category, field_name)
    field_definition = server.send_message(msg)
    return field_definition


def fetch_field_definition(category: str, field_name: str, server: DDEServer) -> CmcFieldDefinition:
    field_definition_res = _fetch_field_defintion_raw(category, field_name, server)
    field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
    return field_definition


def fetch_category_field_definitions_dir(category: str, server: DDEServer) -> CmcDefsDict:
    """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
    fields_definitions = CmcDefsDict()
    for field_name in fetch_field_names(category, server):
        field_definition_res = _fetch_field_defintion_raw(category, field_name, server)
        field_definition = CmcFieldDefinition.from_field_info(field_definition_res)
        fields_definitions[field_name] = field_definition
    return fields_definitions


def get_item_dict(category, pk_value, server: DDEServer) -> dict[str, str]:
    item_dict = {}
    field_defs = fetch_category_field_definitions_dir(category, server)
    field_names = list(field_defs.keys())

    master_msg = get_fields(category=category, item=pk_value, fields=field_names, delim=DELIM)

    if len(str(master_msg)) < 256:
        res = server.send_message(master_msg)
        for attr, value in zip(field_names, res):
            item_dict[attr] = value
    else:
        for start in range(0, len(field_names), MAX_FIELDS_CHUNK):
            fields_chunk = field_names[start:start + MAX_FIELDS_CHUNK]
            chunk_msg = get_fields(category=category, item=pk_value, fields=fields_chunk, delim=DELIM)
            chunk_res = server.send_message(chunk_msg)
            for attr, value in zip(fields_chunk, chunk_res):
                item_dict[attr] = value
    assert len(item_dict) == len(field_names)
    return item_dict
