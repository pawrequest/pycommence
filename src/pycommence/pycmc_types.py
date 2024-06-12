from __future__ import annotations

import typing as _t
from dataclasses import dataclass
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

# from pycommence.api import csr_api

FilterConditionType = Literal['Equal To', 'Contains', 'After']
FilterType = Literal['F', 'CTI', 'CTCF', 'CTCTI']
NotFlagType = Literal['Not', '']


class FilterArray(BaseModel):
    """Array of Cursor Filters."""

    filters: dict[int, CmcFilter] = Field(default_factory=dict)

    def add_replace_filters(self, *filters: CmcFilter):
        """Add Filters by their index. Overwrites if index exists."""
        for i, fil in enumerate(filters):
            self.filters[i + 1] = fil
        return self


class CmcFilter(BaseModel):
    """Cursor Filter."""
    cmc_col: str
    f_type: FilterType = 'F'
    value: str = ''
    condition: FilterConditionType = 'Equal To'
    not_flag: NotFlagType = ''

    @model_validator(mode='after')
    def condition_val(self):
        """ Validate Condition and Value.
        Value must be set when condition is 'Contains' or 'Equal To'
        """
        if self.condition == 'Contains' or self.condition == 'Equal To':
            if not self.value:
                raise ValueError('Value must be set when condition is "Contains"')
        self.value = f', "{self.value}"' if self.value else ''

    def filter_str(self, slot: int) -> str:
        filter_str = (
            f'[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self.cmc_col}, {self.condition}{self.value})]'
        )
        return filter_str


@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


class CmcError(Exception):
    def __init__(self, msg='Commence is not installed'):
        self.msg = msg
        super().__init__(self.msg)


CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def get_cmc_date(datestr: str):
    """Use CMC Cannonical flag"""
    if isinstance(datestr, datetime):
        return datestr.date()
    elif isinstance(datestr, date):
        return datestr
    elif isinstance(datestr, str):
        if datestr.isdigit():
            if len(datestr) == 8:
                return datetime.strptime(datestr, CmcDateFormat).date()
        if len(datestr) == 10:
            return datetime.fromisoformat(datestr).date()


def get_cmc_time(time_str: str):
    """ Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()


EmptyKind = _t.Literal['ignore', 'raise']
