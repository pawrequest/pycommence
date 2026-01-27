from typing import Any

from pycommence.client_dde.dde_server import DDEServer
from pycommence.client_dde.pycmc_dde.dde_request import (
    dde_get_field_definition,
    dde_get_field_names,
    dde_get_fields,
)
from pycommence.client_dde.pycmc_dde.routines import MAX_FIELDS_CHUNK, get_pk
from pycommence.fields import CmcDefsDict, CmcFieldDefinition, DELIM
from pycommence.client_dde.directory import request_msgs


def fetch_field_names(category: str, server: DDEServer) -> bool | str | list[str]:
    msg = request_msgs.get_field_names(category)
    field_names = server.send_message(msg)
    return field_names


def fetch_field_defintion(category: str, field_name: str, server) -> bool | str | list[str]:
    msg = request_msgs.get_field_definition(category, field_name)
    field_definition = server.send_message(msg)
    return field_definition


def fetch_category_field_definitions_dir(category: str, server: DDEServer) -> CmcDefsDict:
    """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
    fields_definitions = CmcDefsDict()
    for field_name in fetch_field_names(category, server):
        field_definition_res = fetch_field_defintion(category, field_name, server)
        field_definition = CmcFieldDefinition.from_field_info(field_definition_res, DELIM)
        fields_definitions[field_name] = field_definition
    return fields_definitions


def get_item_routine2(category, pk_value, conv) -> dict[str, str]:
    # PYTHON DDE NOT COMMENCE
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
    # PYTHON DDE NOT COMMENCE
    field_defs = {}
    for field in field_names:
        finfo: list = conv.Request(dde_get_field_definition('Contact', field))
        fdef = CmcFieldDefinition.from_field_info(finfo, DELIM)
        field_defs[field] = fdef
    return field_defs
