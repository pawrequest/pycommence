# from __future__ import annotations
from __future__ import annotations

import datetime
import enum
import pathlib
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, IntEnum, StrEnum, auto
from typing import Literal
from _decimal import Decimal

import pydantic as _p
import pythoncom
from pydantic import BaseModel, Field

# from pycommence.api import csr_api

FilterConditionType = Literal['Equal To', 'Contains', 'After', 'Between', 'Before', 'Not Equal To', 'Not Contains']
FilterType = Literal['F', 'CTI', 'CTCF', 'CTCTI']
NotFlagType = Literal['Not', '']


class ConditionType(StrEnum):
    EQUAL = 'Equal To'
    CONTAIN = 'Contains'
    AFTER = 'After'
    BETWEEN = 'Is Between'
    BEFORE = 'Before'
    NOT_EQUAL = 'Not Equal To'
    NOT_CONTAIN = 'Not Contains'
    ON = 'On'


class NoneFoundHandler(StrEnum):
    ignore = auto()
    error = auto()


class RadioType(StrEnum):
    HYT = 'Hytera Digital'
    K_UHF = 'Kirisun UHF'
    K_VHF = 'Kirisun VHF'
    TES_289 = 'Tesunho SIM TH289'
    TES_288 = 'Tesunho SIM TH288'
    TES_389 = 'Tesunho SIM TH388'


class CmcFilter(BaseModel):
    """Cursor Filter."""

    cmc_col: str
    f_type: FilterType = 'F'
    value: str = ''
    condition: ConditionType = 'Equal To'
    not_flag: NotFlagType = ''

    def __str__(self):
        return self.filter_str(0)

    def filter_str(self, slot: int) -> str:
        filter_str = f'[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self.cmc_col}, {self.condition}{f', {self.value}' if self.value else ''})]'
        return filter_str


class SortOrder(StrEnum):
    ASC = 'Ascending'
    DESC = 'Descending'


class FilterArray(BaseModel):
    """Array of Cursor Filters."""

    filters: dict[int, CmcFilter] = Field(default_factory=dict)
    sorts: tuple[tuple[str, SortOrder], ...] = Field(default_factory=tuple)
    sortby: str | None = None
    logic: str | None = None

    @property
    def sorts_txt(self):
        return ', '.join([f'{col}, {order.value}' for col, order in self.sorts])

    @property
    def filter_strs(self):
        return [fil.filter_str(slot) for slot, fil in self.filters.items()]

    def update(self, pkg: dict):
        self.filters.update(pkg)

    def add_filter(self, cmc_filter: CmcFilter):
        if len(self.filters) >= 8:
            raise ValueError('FilterArray can only have 8 filters')
        self.filters[len(self.filters) + 1] = cmc_filter

    def add_filters(self, *filters: CmcFilter):
        for cmcfilter in filters:
            self.add_filter(cmcfilter)

    @classmethod
    def from_filters(cls, *filters: CmcFilter, sorts=None, logic: str | None = None):
        filters_ = {i: fil for i, fil in enumerate(list(filters), 1)}
        filaray = cls(filters=filters_)
        if sorts:
            filaray.sorts = sorts
        if logic:
            filaray.logic = logic
        return filaray

    def __str__(self):
        return ', '.join([str(fil) for fil in self.filters.values()])


@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def to_cmc_date(datecheck: date):
    return datecheck.strftime(CmcDateFormat)


def get_cmc_date(v: str) -> date:
    """Use CMC Cannonical flag"""
    if isinstance(v, datetime):
        return v.date()
    elif isinstance(v, date):
        return v
    elif isinstance(v, str):
        if v.isdigit():
            if len(v) == 8:
                return datetime.strptime(v, CmcDateFormat).date()
        if len(v) in [7, 10]:
            return datetime.fromisoformat(v).date()


def get_cmc_time(time_str: str):
    """Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()


class CursorType(IntEnum):
    """Commence Cursor Types to view based on category, view, or preferences."""

    # open based on a category, columns = all supported fields in the category (in no particular order).
    CATEGORY = 0

    # Valid view-types: report, grid, report viewer, and book/address book.
    # inherit the view's filter, sort, and column set.
    # ICommenceCursor methods can be used to change these attributes.
    VIEW = 1

    # All Pilot* cursor column-sets =  defined by the Commence preferences (in no particular order).
    # It is not possible to change the filter, sort, or column set.

    # Category and fields defined by Preferences-> Other Apps -> 3Com Pilot Address Book.
    PILOT_ADDRESS = 2

    # Category and fields defined by Preferences-> Other Apps -> 3Com Pilot Memo Pad.
    PILOT_MEMO = 3

    # Category and fields defined by Preferences -> Other Apps -> 3Com Pilot To Do List.
    PILOT_TODO = 5

    # Category and fields defined by Preferences -> Other Apps -> 3Com Pilot Date Book.
    PILOT_APPOINT = 6

    # MS Outlook contacts preference
    OUTLOOK_ADDRESS = 7

    # MS Outlook calendar preference
    OUTLOOK_APPOINT = 8

    # MS Outlook Email Log preference
    OUTLOOK_EMAIL_LOG = 9

    # MS Outlook Task preference
    OUTLOOK_TASK = 10

    # open based on the view data used with the Send Letter command
    LETTER_MERGE = 11


class Bookmark(Enum):
    """Starting point for cursor seek operations."""

    BEGINNING = 0
    CURRENT = 1
    END = 2


class OptionFlag(Enum):
    """Flags for get_record and get_value methods."""

    NONE = 0
    FIELD_NAME = 0x0001
    ALL = 0x0002
    SHARED = 0x0004
    PILOT = 0x0008
    CANONICAL = 0x0010
    INTERNET = 0x0020


class OptionFlagInt(IntEnum):
    """Flags for get_record and get_value methods."""

    NONE = 0
    FIELD_NAME = 0x0001
    ALL = 0x0002
    SHARED = 0x0004
    PILOT = 0x0008
    CANONICAL = 0x0010
    INTERNET = 0x0020


FLAGS_UNUSED = 0
DELIM = r';*;%'


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
            combobox=flags[6] == '1',
            shared=flags[7] == '1',
            mandatory=flags[8] == '1',
            recurring=flags[9] == '1',
            max_chars=int(max_chars),
            default_string=default_string,
        )
