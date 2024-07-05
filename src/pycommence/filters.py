from __future__ import annotations

from abc import ABC
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field

from pycommence.pycmc_types import Connection2

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
    NOT = 'Not'


class CmcFilter(BaseModel, ABC):
    f_type: FilterType
    not_flag: NotFlagType = ''
    value: str = ''

    def view_filter_str(self, slot=1):
        return f'[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self._filter_str})]'

    def __str__(self):
        return self._filter_str

    @property
    def _filter_str(self):
        raise NotImplementedError()


class FieldFilter(CmcFilter):
    """Cursor Filter."""

    f_type: Literal['F'] = 'F'
    column: str
    condition: ConditionType = 'Equal To'

    @property
    def _filter_str(self) -> str:
        filter_str = f'{self.column}, {self.condition}{f', "{self.value}"' if self.value else ''}'
        return filter_str


class ConnectedItemFilter(FieldFilter):
    f_type: Literal['CTI'] = 'CTI'
    connection_category: str

    # column is relationship name eg 'Relates To'

    @property
    def _filter_str(self) -> str:
        return f'{self.column}, {self.connection_category}, "{self.value}"'


class ConnectedFieldFilter(ConnectedItemFilter):
    f_type: Literal['CTCF'] = 'CTCF'
    connected_column: str

    @property
    def _filter_str(self):
        return f'{self.column}, {self.connection_category}, {self.connected_column}, {self.condition}, "{self.value}"'


class ConnectedItemConnectedItemFilter(ConnectedFieldFilter):
    f_type: Literal['CTCTI'] = 'CTCTI'
    connection_column_2: str
    connection_category_2: str

    @property
    def _filter_str(self) -> str:
        return f'{self.column}, {self.connection_category}, {self.connection_column_2}, {self.connection_category_2}, "{self.value}"'


class SortOrder(StrEnum):
    ASC = 'Ascending'
    DESC = 'Descending'


Logic = Literal['Or', 'And']


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
    def view_sort_text(self):
        return f'[ViewSort({self.sorts_txt})]'

    @property
    def sort_logic_text(self):
        return f'[ViewConjunction({self.logic})]'

    @property
    def filter_strs(self):
        return [fil.view_filter_str(slot) for slot, fil in self.filters.items()]

    def update(self, pkg: dict):
        self.filters.update(pkg)

    def add_filter(self, cmc_filter: FieldFilter):
        next_empty = next((i for i in range(1, 9) if i not in self.filters), None)
        if next_empty:
            self.filters[next_empty] = cmc_filter
        else:
            raise ValueError('No empty slots available')

    def add_filters(self, *filters: FieldFilter):
        for cmcfilter in filters:
            self.add_filter(cmcfilter)

    @classmethod
    def from_filters(cls, *filters: FieldFilter, sorts=None, logic: str | None = None):
        filters_ = {i: fil for i, fil in enumerate(list(filters), 1)}
        filaray = cls(filters=filters_)
        if sorts:
            filaray.sorts = sorts
        if logic:
            filaray.logic = logic
        return filaray

    def __str__(self):
        filstrs = [str(fil) for fil in self.filters.values()]
        return ', '.join(filstrs)


def field_fil_to_confil(field_fil: FieldFilter, connection: Connection2):
    hireconfil = ConnectedFieldFilter(
        column=connection.name,
        connection_category=connection.category,
        connected_column=field_fil.column,
        condition=field_fil.condition,
        value=field_fil.value,
    )
    return hireconfil.model_validate(hireconfil, from_attributes=True)
