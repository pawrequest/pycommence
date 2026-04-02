from __future__ import annotations

import pathlib
from dataclasses import dataclass
from datetime import time
from decimal import Decimal
from typing import Literal, NamedTuple

from loguru import logger

from pycommence.core.types import CommenceDateOptional
from pycommence.pycommence_options import get_options

# DELIM = r';*;%'
DELIM = get_options().delim


def parse_info_str(field_info: str | list[str], delim: str = DELIM) -> tuple[str, str, str, str]:
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
            type=CmcDataType.lookup_datatype('CONNECTION'),
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
            type=CmcDataType.lookup_datatype('ERROR'),
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
        datatype = CmcDataType.lookup_datatype(field_type_str)
        if not datatype:
            logger.warning(f'Unknown field type: {field_type_str} - returning ERROR field definition')
            return cls.error_field()
        return cls(
            type=datatype,
            combobox=flags[6] == '1',
            shared=flags[7] == '1',
            mandatory=flags[8] == '1',
            recurring=flags[9] == '1',
            max_chars=int(max_chars),
            default_string=default_string,
        )


class CmcDefsDict(dict[str, CmcFieldDefinition]):
    """Field Name to CmcFieldDefinition."""

    _name_field: str | None = None

    def name_field(self, error: Literal['raise', 'ignore'] = 'raise') -> str | None:
        if self._name_field:
            return self._name_field

        defs = [(name, field_def) for name, field_def in self.items() if field_def.type.alias == 'NAME']
        if len(defs) == 1:
            self._name_field = defs[0][0]
            return self._name_field
        else:
            if error != 'ignore':
                raise RuntimeError(f'Expected exactly one NAME field in definitions - found {len(defs)}:{defs}.')

        return self._name_field

    def py_types_dict(self) -> dict[str, type]:
        return {k: v.type.py_type for k, v in self.items()}


class CmcDataType(NamedTuple):
    int_value: int
    alias: str
    py_type: type

    @classmethod
    def unknown(cls) -> CmcDataType:
        return CmcDataType(-1, 'ERROR', str)

    @classmethod
    def lookup_datatype(cls, thingy: int | str | type) -> CmcDataType:
        try:
            inty = int(thingy)
            return INT_TO_DEF.get(inty, cls.unknown())
        except (ValueError, TypeError):
            pass
        if isinstance(thingy, str):
            return ALIAS_TO_DEF.get(thingy.upper(), cls.unknown())
        elif isinstance(thingy, type):
            return TYPE_TO_DEF.get(thingy, cls.unknown())
        raise ValueError(f'Unknown thingy type: {type(thingy)}')


DATA_TYPES: list[CmcDataType] = [
    CmcDataType(0, 'TEXT', str),
    CmcDataType(1, 'NUMBER', Decimal),
    CmcDataType(2, 'DATE', CommenceDateOptional),
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
    CmcDataType(24, 'URL', str),
    CmcDataType(17, 'CONNECTION', str),
]
INT_TO_DEF = {fd.int_value: fd for fd in DATA_TYPES}
ALIAS_TO_DEF = {fd.alias: fd for fd in DATA_TYPES}
TYPE_TO_DEF = {fd.py_type: fd for fd in DATA_TYPES}

# def lookup_datatype(thingy: int | str | type) -> CmcDataType:
#     try:
#         inty = int(thingy)
#         return INT_TO_DEF.get(inty)
#     except (ValueError, TypeError):
#         pass
#     if isinstance(thingy, str):
#         return ALIAS_TO_DEF.get(thingy.upper())
#     elif isinstance(thingy, type):
#         return TYPE_TO_DEF.get(thingy)
#     raise ValueError(f'Unknown thingy type: {type(thingy)}')
