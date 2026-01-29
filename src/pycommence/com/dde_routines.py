from typing import Any

from pycommence import PyCommence, pycommence_context
from pycommence.dde.msgs import view as view_msgs, get as request_msgs
from pycommence.dde.dde_errors import PyCommenceDDEError
from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition, DELIM



MAX_FIELDS_CHUNK = 15  # undocumented limit in Commence DDE for GetFields
MAX_CMD_LEN = 256  # undocumented limit in Commence DDE for command length


def get_item_routine(category, pk_value) -> dict[str, str]:
    with pycommence_context() as p:
        field_defs_dict = fetch_category_field_definitions(category)
        primary_key = get_pk(category, field_defs_dict)
        field_defs_filtered = field_defs_dict

        filter_by_pk_contains(category, p, pk_value, primary_key)
        to_fetch = list(field_defs_filtered.keys())
        item_dict = {}
        for start in range(0, len(to_fetch), MAX_FIELDS_CHUNK):
            fields_chunk = to_fetch[start:start + MAX_FIELDS_CHUNK]
            try:
                chunk_msg = request_msgs.get_fields(category, pk_value, fields_chunk, DELIM)
                chunk_res = p.send_dde_msg(chunk_msg)
                for fname, fvalue in zip(fields_chunk, chunk_res):
                    item_dict[fname] = fvalue
            except PyCommenceDDEError as e:
                raise RuntimeError(
                    f'Failed to get fields for {category} where {primary_key} contains {pk_value}. Last attempted field: {last} of type {failed_type}'
                ) from e
        return item_dict


def filter_by_pk_contains(category, p: PyCommence, pk_value, primary_key: str):
    set_category(category, p)
    msg = view_msgs.view_filter(1, 'F', None, primary_key, 'Contains', pk_value)
    assert p.send_dde_msg(
        msg
    ) == 'OK', f'Failed to set view filter for {category} where {primary_key} contains {pk_value}'


def set_category(category, p: PyCommence):
    msg = view_msgs.view_category(category)
    assert p.send_dde_msg(msg) == 'OK', f'Failed to set view category to {category}'


def get_pk(category, field_defs_dict: dict[str, CmcFieldDefinition]) -> str:
    _primary_keys = [fname for fname, finfo in field_defs_dict.items() if finfo.type.alias == 'NAME']
    assert len(
        _primary_keys
    ) == 1, f'Expected exactly one primary key field for category {category}, found {_primary_keys}'
    primary_key: str = _primary_keys[0]
    return primary_key


def fetch_category_field_definitions(category: str, pycmc: PyCommence | None = None) -> CmcDefsDict:
    """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
    fields_definitions = CmcDefsDict()
    # noinspection PydanticTypeChecker
    with pycmc or pycommence_context() as p:
        for field_name in fetch_field_names(category, p):
            field_definition_res = fetch_defintion(category, field_name, p)
            field_definition = CmcFieldDefinition.from_field_info(field_definition_res, DELIM)
            fields_definitions[field_name] = field_definition
    return fields_definitions


def fetch_field_names(category: str, p: PyCommence | Any) -> bool | str | list[str]:
    msg = request_msgs.get_field_names(category)
    return p.send_dde_msg(msg)


def fetch_defintion(category: str, field_name: str | Any, p: PyCommence | Any) -> bool | str | list[str]:
    # dde_cmd = dde_get_field_definition(category, field_name)
    # field_def_res = p.send_dde(cmd=dde_cmd, topic=DDETopic.GET, kind=DDEKind.REQUEST)
    msg = request_msgs.get_field_definition(category, field_name)
    field_def_res = p.send_dde_msg(msg)
    return field_def_res
