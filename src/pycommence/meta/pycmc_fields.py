from __future__ import annotations

import pathlib
from dataclasses import dataclass
from datetime import date, time
from decimal import Decimal
from typing import NamedTuple

from loguru import logger
from pydantic import HttpUrl

DELIM = r';*;%'


def parse_info_str(field_info: str | list[str], delim: str = DELIM, ) -> tuple[str, str, str, str]:
    if isinstance(field_info, str):
        parts = field_info.split(delim)
    else:
        parts = field_info
    field_type_str = parts[0]
    flags = parts[1]
    max_chars = parts[2]
    default_string = parts[3]
    if other := parts[4:]:
        logger.warning(f'Ignoring extra field info parts: {other}')
    return default_string, field_type_str, flags, max_chars


@dataclass
class CmcFieldDefinition:
    type: CmcDataType
    combobox: bool
    shared: bool
    mandatory: bool
    recurring: bool
    max_chars: int
    default_string: str = ''

    @classmethod
    def connection_field(cls) -> CmcFieldDefinition:
        return cls(
            type=lookup_field_definition('CONNECTION'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=0,
            default_string='',
        )

    @classmethod
    def error_field(cls) -> CmcFieldDefinition:
        return cls(
            type=lookup_field_definition('ERROR'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=0,
            default_string='',
        )

    @classmethod
    def from_field_info(cls, field_info: str | list[str], delim: str = DELIM) -> CmcFieldDefinition:
        default_string, field_type_str, flags, max_chars = parse_info_str(field_info, delim)
        field_def = lookup_field_definition(field_type_str)
        if not field_def:
            logger.warning(f'Unknown field type: {field_type_str} - returning ERROR field definition')
            return cls.error_field()
        return cls(
            type=field_def,
            combobox=flags[6] == '1',
            shared=flags[7] == '1',
            mandatory=flags[8] == '1',
            recurring=flags[9] == '1',
            max_chars=int(max_chars),
            default_string=default_string,
        )




class CmcDataType(NamedTuple):
    int_value: int
    alias: str
    py_type: type


FIELD_DEFS: list[CmcDataType] = [
    CmcDataType(0, 'TEXT', str),
    CmcDataType(1, 'NUMBER', Decimal),
    CmcDataType(2, 'DATE', date),
    CmcDataType(3, 'TELEPHONE', str),
    CmcDataType(7, 'CHECKBOX', bool),
    CmcDataType(11, 'NAME', str),
    CmcDataType(12, 'DATAFILE', pathlib.Path),
    CmcDataType(13, 'IMAGE', pathlib.Path),
    CmcDataType(14, 'TIME', time),
    CmcDataType(15, 'EXCEL_CELL', str),
    CmcDataType(20, 'CALCULATION', str),
    CmcDataType(21, 'SEQUENCE', int),
    CmcDataType(22, 'SELECTION', str),
    CmcDataType(23, 'EMAIL', str),
    CmcDataType(24, 'URL', HttpUrl),
    CmcDataType(17, 'CONNECTION', str)
]
INT_TO_DEF = {fd.int_value: fd for fd in FIELD_DEFS}
ALIAS_TO_DEF = {fd.alias: fd for fd in FIELD_DEFS}
TYPE_TO_DEF = {fd.py_type: fd for fd in FIELD_DEFS}


def lookup_field_definition(thingy: int | str | type) -> CmcDataType:
    try:
        inty = int(thingy)
        return INT_TO_DEF.get(inty)
    except (ValueError, TypeError):
        pass
    if isinstance(thingy, str):
        return ALIAS_TO_DEF.get(thingy.upper())
    elif isinstance(thingy, type):
        return TYPE_TO_DEF.get(thingy)
    raise ValueError(f'Unknown thingy type: {type(thingy)}')


class CmcDefsDict(dict[str, CmcFieldDefinition]):
    """Field Name to CmcFieldDefinition."""

    def py_types_dict(self) -> dict[str, type]:
        return {k: v.type.py_type for k, v in self.items()}
