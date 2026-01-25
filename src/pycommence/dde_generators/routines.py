from typing import Any

import win32ui  # noqa

from pycommence import PyCommence, pycommence_context
from pycommence.dde_generators.dde_request import dde_get_field_definition, dde_get_field_names, dde_get_fields
from pycommence.dde_generators.view import dde_view_category, dde_view_filter
from pycommence.exceptions import PyCommenceDDEError
from pycommence.meta.pycmc_fields import CmcFieldDefinition, CmcFieldType, DELIM
from pycommence.wrapper.conversation_wrapper import DDEKind, DDETopic

MAX_FIELDS_CHUNK = 15  # undocumented limit in Commence DDE for GetFields
MAX_CMD_LEN = 256  # undocumented limit in Commence DDE for command length
FETCH_FIELDS = {CmcFieldType.TEXT, CmcFieldType.NUMBER, CmcFieldType.DATE, CmcFieldType.CHECKBOX, CmcFieldType.DATAFILE,
                CmcFieldType.IMAGE, CmcFieldType.NAME, CmcFieldType.TELEPHONE}


def get_item_routine(category, pk_value) -> dict[str, str]:
    with pycommence_context() as p:  # noqa
        field_defs_dict = get_field_definitions(category)
        primary_key = get_pk(category, field_defs_dict)
        # field_defs_filtered = {fname: finfo for fname, finfo in field_defs_dict.items() if
        #                        finfo.type in FETCH_FIELDS}
        field_defs_filtered = field_defs_dict

        filter_routine(category, p, pk_value, primary_key)
        to_fetch = list(field_defs_filtered.keys())
        resd = {}
        for start in range(0, len(to_fetch), MAX_FIELDS_CHUNK):
            fields_chunk = to_fetch[start:start + MAX_FIELDS_CHUNK]
            try:
                chunk_res = p.send_dde(
                    cmd=dde_get_fields(category=category, item=pk_value, fields=fields_chunk, delim=DELIM),
                    topic=DDETopic.VIEW_DATA
                )
                for fname, fvalue in zip(fields_chunk, chunk_res):
                    resd[fname] = fvalue
            except PyCommenceDDEError as e:
                last = fields_chunk[-1]
                failed_type = field_defs_dict[last]
                raise RuntimeError(
                    f"Failed to get fields for {category} where {primary_key} contains {pk_value}. Last attempted field: {last} of type {failed_type}"
                ) from e
        return resd


def get_item_routine2(category, pk_value, conv) -> dict[str, str]:
    field_names = conv.Request(dde_get_field_names(category)).split(DELIM)
    field_defs = get_defs(conv, field_names)

    primary_key = get_pk(category, field_defs)

    to_fetch = list(field_defs.keys())
    lent_to_fetch = len(','.join(to_fetch))
    resd = {}
    dde_cmds_list = []
    dde_cmd_master = dde_get_fields(category=category, item=pk_value, fields=to_fetch, delim=DELIM)
    if len(dde_cmd_master) > 256:
        dde_cmds_list = [dde_cmd_master]
    else:
        for start in range(0, len(to_fetch), MAX_FIELDS_CHUNK):
            fields_chunk = to_fetch[start:start + MAX_FIELDS_CHUNK]
            chunk_cmd = dde_get_fields(category=category, item=pk_value, fields=fields_chunk, delim=DELIM)
            dde_cmds_list.append(chunk_cmd)
    for chunk_cmd in dde_cmds_list:
        chunk_rows = conv.Request(chunk_cmd)
        # for fname, fvalue in zip(fields_chunk, chunk_rows):
        #     resd[fname] = fvalue
    # except dde.error as e:
    #     raise RuntimeError(
    #         f"CMD_LEN = {len(dde_cmd)}Failed to get fields for {category} where {primary_key} contains {pk_value}. Last attempted field: {fields_chunk[-1]}"
    #     ) from e
    return resd


def get_defs(conv, field_names) -> dict[Any, Any]:
    field_defs = {}
    for field in field_names:
        finfo: list = conv.Request(dde_get_field_definition('Contact', field))
        fdef = CmcFieldDefinition.from_field_info(finfo, DELIM)
        field_defs[field] = fdef
    return field_defs


def filter_routine(category, p: PyCommence, pk_value, primary_key: str):
    if not p.send_dde(cmd=dde_view_category(category)) == 'OK':
        raise RuntimeError(f"Failed to set view category to {category}")
    if not p.send_dde(
            cmd=(dde_view_filter(
                1, 'F', None, primary_key, 'Contains', pk_value
            ))
    ) == 'OK':
        raise RuntimeError(f"Failed to set view filter for {category} where {primary_key} contains {pk_value}")


def filter_routine2(category, p: PyCommence, pk_value, primary_key: str):
    if not p.send_dde(cmd=dde_view_category(category), topic=DDETopic.VIEW_DATA) == 'OK':
        raise RuntimeError(f"Failed to set view category to {category}")
    if not p.send_dde(
            cmd=(dde_view_filter(
                1, 'F', None, primary_key, 'Contains', pk_value
            )), topic=DDETopic.VIEW_DATA
    ) == 'OK':
        raise RuntimeError(f"Failed to set view filter for {category} where {primary_key} contains {pk_value}")


def get_pk(category, field_defs_dict: dict[str, CmcFieldDefinition]) -> str:
    _primary_keys = [fname for fname, finfo in field_defs_dict.items() if finfo.type == CmcFieldType.NAME]
    assert len(
        _primary_keys
    ) == 1, f"Expected exactly one primary key field for category {category}, found {_primary_keys}"
    primary_key: str = _primary_keys[0]
    return primary_key


def get_field_definitions(category: str) -> dict[str, CmcFieldDefinition]:
    fields_defs = {}

    dde_get_fields = dde_get_field_names('Contact')
    with pycommence_context() as p:  # noqa
        field_names = p.send_dde(cmd=dde_get_fields, topic='Tutorial', kind=DDEKind.REQUEST)
        for field_name in field_names:
            dde_cmd = dde_get_field_definition('Contact', field_name)
            field_def_res = p.send_dde(cmd=dde_cmd, topic='Tutorial', kind=DDEKind.REQUEST)
            finfo = CmcFieldDefinition.from_field_info(field_def_res, DELIM)
            fields_defs[field_name] = finfo
    return fields_defs
# [_ for _ in fields_defs.values() if _.type in [CmcFieldType.TEXT]]
