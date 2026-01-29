from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, IntEnum, StrEnum
from typing import Annotated, Any

from pydantic import BeforeValidator

FLAGS_UNUSED = 0


class NoneFoundHandler(StrEnum):
    ignore = 'IGNORE'
    error = 'ERROR'


class SeekBookmark(Enum):
    """Starting point for cursor seek operations."""

    BEGINNING = 0
    CURRENT = 1
    END = 2


@dataclass
class Connection:
    name: str
    from_table: str
    from_field: str
    to_table: str
    to_field: str


@dataclass
class ConnectedColumn:
    name: str
    category: str
    column: str


CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def to_cmc_date(datecheck: date):
    return datecheck.strftime(CmcDateFormat)


def get_cmc_date_maybe(v: Any) -> date | None:
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
    print(f'No date found: {v}')
    return None


def get_cmc_date(v: str) -> date | None:
    """Use CMC Cannonical flag"""
    if converted := get_cmc_date_maybe(v):
        return converted
    raise ValueError(f'No date found: {v}')


def get_cmc_time(time_str: str):
    """Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()


CommenceDateOptional = Annotated[date | None, BeforeValidator(get_cmc_date_maybe)]
CommenceDate = Annotated[date, BeforeValidator(get_cmc_date)]


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
