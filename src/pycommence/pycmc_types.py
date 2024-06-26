from __future__ import annotations

import typing as _t
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum, auto
from typing import Literal

from pydantic import BaseModel, Field, model_validator

# from pycommence.api import csr_api

FilterConditionType = Literal['Equal To', 'Contains', 'After', 'Between', 'Before', 'Not Equal To', 'Not Contains']
FilterType = Literal['F', 'CTI', 'CTCF', 'CTCTI']
NotFlagType = Literal['Not', '']


class ConditionType(StrEnum):
    EQUAL = 'Equal To'
    CONTAIN = 'Contains'
    AFTER = 'After'
    BETWEEN = 'Between'
    BEFORE = 'Before'
    NOT_EQUAL = 'Not Equal To'
    NOT_CONTAIN = 'Not Contains'
    ON = 'On'


class NoneFoundHandler(StrEnum):
    ignore = auto()
    error = auto()


class RadioType(StrEnum):
    HYT = 'Hytera Digital'


class FilterArray(BaseModel):
    """Array of Cursor Filters."""

    filters: dict[int, CmcFilter] = Field(default_factory=dict)

    def add_replace_filters(self, *filters: CmcFilter):
        """Add Filters by their index. Overwrites if index exists."""
        for i, fil in enumerate(filters):
            self.filters[i + 1] = fil
        return self

    def __str__(self):
        return ', '.join([str(fil) for fil in self.filters.values()])


class CmcFilter(BaseModel):
    """Cursor Filter."""

    cmc_col: str
    f_type: FilterType = 'F'
    value: str = ''
    condition: FilterConditionType | ConditionType = 'Equal To'
    not_flag: NotFlagType = ''
    value_set: bool = False

    def __str__(self):
        return f'{self.cmc_col} {self.not_flag} {self.condition} {self.value}'

    @model_validator(mode='after')
    def condition_val(self):
        """Validate Condition and Value.
        Value must be set when condition is 'Contains' or 'Equal To'
        """
        if self.value_set:
            return self
        # if self.condition == 'Contains' or self.condition == 'Equal To':
        #     if not self.value:
        #         raise ValueError('Value must be set when condition is "Contains"')
        self.value = f', "{self.value}"' if self.value else ''
        self.value_set = True
        return self

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
    def __init__(self, msg: str = ''):
        self.msg = msg
        super().__init__(self.msg)


class PyCommenceError(Exception):
    pass


class PyCommenceExistsError(PyCommenceError):
    pass


class PyCommenceNotFoundError(PyCommenceError):
    pass


class PyCommenceMaxExceededError(PyCommenceError):
    pass


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


EmptyKind = _t.Literal['ignore', 'raise']
