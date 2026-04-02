from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

import pydantic as _p
from pydantic import BeforeValidator, PlainSerializer

if TYPE_CHECKING:
    pass

CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def to_cmc_date(datecheck: date | None):
    return datecheck.strftime(CmcDateFormat) if datecheck else ''


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


def get_cmc_time(time_str: str):
    """Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()


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


def replace_noncompliant_apostrophes(value: str) -> str:
    value = str(value)
    if isinstance(value, str):
        noncompliant_apostrophes = ['’', '‘', '′', 'ʼ', '´']
        for char in noncompliant_apostrophes:
            value = value.replace(char, "'")
    if value is None:
        return ''
    return value


def split_csv(v):
    if isinstance(v, list):
        return v
    if isinstance(v, str):
        v = replace_noncompliant_apostrophes(v)
        return [item.strip() for item in v.split(',') if item.strip()]
    raise ValueError(f'Expected a string, got {type(v)}')


def join_csv(v, separator=', '):
    if isinstance(v, str):
        return v
    if isinstance(v, list):
        return separator.join(v)
    raise ValueError(f'Expected a list, got {type(v)}')


join_lines = partial(join_csv, separator=',\r\n')
join_spaces = partial(join_csv, separator=', ')

# TYPES
CSVLines = Annotated[list[str], BeforeValidator(split_csv), PlainSerializer(join_lines)]
CSVSpaces = Annotated[list[str], BeforeValidator(split_csv), PlainSerializer(join_spaces)]
CommenceString = Annotated[str, BeforeValidator(replace_noncompliant_apostrophes)]
CommenceDateMaybe = Annotated[date | None, _p.BeforeValidator(get_cmc_date_maybe), PlainSerializer(to_cmc_date)]
CommencePath = Annotated[Path, BeforeValidator(lambda x: Path(x)), PlainSerializer(str)]
CommenceConnection = CSVSpaces
