from typing import Any


from pycommence import PyCommence, pycommence_context
from pycommence.client_dde.pycmc_dde.dde_request import dde_get_field_definition, dde_get_field_names, dde_get_fields
from pycommence.client_dde.pycmc_dde.view import dde_view_category, dde_view_filter
from pycommence.exceptions import PyCommenceDDEError
from pycommence.fields import CmcDefsDict, CmcFieldDefinition, DELIM
from pycommence.wrapper.conversation_wrapper import DDEKind, DDETopic

CMC_FIELD_DEF_DICT = dict[str, CmcFieldDefinition]

MAX_FIELDS_CHUNK = 15  # undocumented limit in Commence DDE for GetFields
MAX_CMD_LEN = 256  # undocumented limit in Commence DDE for command length


def get_item_routine(category, pk_value) -> dict[str, str]:
    with pycommence_context() as p:
        field_defs_dict = fetch_category_field_definitions(category)
        primary_key = get_pk(category, field_defs_dict)
        field_defs_filtered = field_defs_dict

        filter_by_pk_contains(category, p, pk_value, primary_key)
        to_fetch = list(field_defs_filtered.keys())
        resd = {}
        for start in range(0, len(to_fetch), MAX_FIELDS_CHUNK):
            fields_chunk = to_fetch[start:start + MAX_FIELDS_CHUNK]
            try:
                chunk_res = p.send_dde(
                    cmd=dde_get_fields(category=category, item=pk_value, fields=fields_chunk, delim=DELIM),
                    topic=DDETopic.VIEW
                )
                for fname, fvalue in zip(fields_chunk, chunk_res):
                    resd[fname] = fvalue
            except PyCommenceDDEError as e:
                last = fields_chunk[-1]
                failed_type = field_defs_dict[last]
                raise RuntimeError(
                    f'Failed to get fields for {category} where {primary_key} contains {pk_value}. Last attempted field: {last} of type {failed_type}'
                ) from e
        return resd


def filter_by_pk_contains(category, p: PyCommence, pk_value, primary_key: str):
    set_category(category, p)
    assert p.send_dde(
        cmd=(dde_view_filter(
            1, 'F', None, primary_key, 'Contains', pk_value
        ))
    ) == 'OK', f'Failed to set view filter for {category} where {primary_key} contains {pk_value}'


def set_category(category, p: PyCommence):
    assert p.send_dde(cmd=dde_view_category(category)) == 'OK', f'Failed to set view category to {category}'


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
    get_fields_cmd = dde_get_field_names(category)
    field_names = p.send_dde(cmd=get_fields_cmd, topic=DDETopic.GET, kind=DDEKind.REQUEST)
    return field_names


def fetch_defintion(category: str, field_name: str | Any, p: PyCommence | Any) -> bool | str | list[str]:
    dde_cmd = dde_get_field_definition(category, field_name)
    field_def_res = p.send_dde(cmd=dde_cmd, topic=DDETopic.GET, kind=DDEKind.REQUEST)
    return field_def_res
