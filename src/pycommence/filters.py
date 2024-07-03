from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

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
        next_empty = next((i for i in range(1, 9) if i not in self.filters), None)
        if next_empty:
            self.filters[next_empty] = cmc_filter
        else:
            raise ValueError('No empty slots available')

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


DELIM = r';*;%'
