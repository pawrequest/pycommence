from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Annotated, Any, Protocol, TYPE_CHECKING

from pydantic import BeforeValidator

if TYPE_CHECKING:
    from pycommence.dde import DDETopic, DDEMessageBase

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

#
# class PyCmcProtocol(Protocol):
#     def item_add(self, category: str, item_name: str, topic: DDETopic) -> bool:
#         ...
#
#     def item_delete(self, category: str, item_name: str, topic: DDETopic) -> bool:
#         ...
