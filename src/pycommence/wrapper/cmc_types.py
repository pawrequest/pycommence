from __future__ import annotations

import datetime
import enum
import pathlib
from decimal import Decimal

import pydantic as _p
import pythoncom

DELIM = r";*;%"


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
    URL = _p.HttpUrl


# CmcFieldDataTypeMap = {
#     'TEXT': str,
#     'NUMBER': Decimal,
#     'DATE': datetime.date,
#     'TELEPHONE': str,
#     'CHECKBOX': bool,
#     'NAME': str,
#     'DATAFILE': pathlib.Path,
#     'IMAGE': pathlib.Path,
#     'TIME': datetime.time,
#     'EXCEL_CELL': str,
#     'CALCULATION': str,
#     'SEQUENCE': int,
#     'SELECTION': str,
#     'EMAIL': str,
#     'URL': _p.HttpUrl
# }


class CmcFieldDefinition(_p.BaseModel):
    type: CmcFieldType
    combobox: bool
    shared: bool
    mandatory: bool
    recurring: bool
    max_chars: int
    default_string: str = ''

    @classmethod
    def from_field_info(cls, field_info: str):
        pythoncom.CoInitialize()  # Initialize COM library on this thread

        parts = field_info.split(DELIM)
        field_type, flags, max_chars, default_string = parts[0], parts[1], parts[2], parts[3]

        return cls(
            type=CmcFieldType(int(field_type)),
            combobox=flags[6] == "1",
            shared=flags[7] == "1",
            mandatory=flags[8] == "1",
            recurring=flags[9] == "1",
            max_chars=int(max_chars),
            default_string=default_string,
        )
