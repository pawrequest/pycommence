from __future__ import annotations

import enum
import pathlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

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
    type: CmcFieldType
    combobox: bool
    shared: bool
    mandatory: bool
    recurring: bool
    max_chars: int
    default_string: str = ''

    @classmethod
    def connection_field(cls) -> CmcFieldDefinition:
        return cls(
            type=CmcFieldType.CONNECTION,
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
            type=CmcFieldType.ERROR,
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
        try:
            field_type = CmcFieldType(int(field_type_str))
        except ValueError:
            logger.warning(f'Unknown field type: {field_type_str}')
            return cls.error_field()
        return cls(
            type=field_type,
            combobox=flags[6] == '1',
            shared=flags[7] == '1',
            mandatory=flags[8] == '1',
            recurring=flags[9] == '1',
            max_chars=int(max_chars),
            default_string=default_string,
        )


class CmcFieldType(enum.Enum):
    TEXT = 0  # Text field.
    NUMBER = 1  # Number field.
    DATE = 2  # Date field.
    TELEPHONE = 3  # Telephone field.
    CHECKBOX = 7  # Check Box field.
    NAME = 11  # Name field (= primary key).
    DATAFILE = 12  # Data File field (= filepath).
    IMAGE = 13  # Image field.
    TIME = 14  # Time field.
    EXCEL_CELL = 15  # Excel cell. (OBSOLETE)
    CALCULATION = 20  # Calculation field.
    SEQUENCE = 21  # Sequence number field.
    SELECTION = 22  # Selection field.
    EMAIL = 23  # E-mail address field.
    URL = 24  # Internet address field.
    CONNECTION = 17  # Connection field. (not in spec but exists irl)
    ERROR = 99  # Error field (not in spec but added to handle weirdness


class CmcFieldDataType(enum.Enum):
    TEXT = str
    NUMBER = Decimal
    DATE = datetime.date
    TELEPHONE = str
    CHECKBOX = bool
    NAME = str
    DATAFILE = pathlib.Path
    IMAGE = pathlib.Path
    TIME = datetime.time
    EXCEL_CELL = str
    CALCULATION = str
    SEQUENCE = int
    SELECTION = str
    EMAIL = str
    URL = HttpUrl
    CONNECTION = str


CmcFieldDataTypeMap = {
    0: CmcFieldDataType.TEXT,
    1: CmcFieldDataType.NUMBER,
    2: CmcFieldDataType.DATE,
    3: CmcFieldDataType.TELEPHONE,
    7: CmcFieldDataType.CHECKBOX,
    11: CmcFieldDataType.NAME,
    12: CmcFieldDataType.DATAFILE,
    13: CmcFieldDataType.IMAGE,
    14: CmcFieldDataType.TIME,
    15: CmcFieldDataType.EXCEL_CELL,
    20: CmcFieldDataType.CALCULATION,
    21: CmcFieldDataType.SEQUENCE,
    22: CmcFieldDataType.SELECTION,
    23: CmcFieldDataType.EMAIL,
    24: CmcFieldDataType.URL,
    17: CmcFieldDataType.CONNECTION
}
