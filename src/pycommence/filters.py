from __future__ import annotations

from abc import ABC
from enum import StrEnum
from typing import Literal

from loguru import logger
from pydantic import BaseModel, Field, model_validator

from pycommence.pycmc_types import Connection2

FilterKind = Literal['F', 'CTI', 'CTCF', 'CTCTI']
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
    kind: FilterKind
    column: str
    value: str = ''
    not_flag: NotFlagType = ''
    condition: ConditionType = 'Equal To'

    def view_filter_str(self, slot=1):
        return f'[ViewFilter({slot}, {self.kind}, {self.not_flag}, {self._filter_str})]'

    def __str__(self):
        return self.view_filter_str(0)

    @property
    def _filter_str(self):
        raise NotImplementedError()


class FieldFilter(CmcFilter):
    """Cursor Filter."""

    kind: Literal['F'] = 'F'

    @property
    def _filter_str(self) -> str:
        filter_str = f'{self.column}, {self.condition}{f', "{self.value}"' if self.value else ''}'
        return filter_str


class ConnectedItemFilter(FieldFilter):
    kind: Literal['CTI'] = 'CTI'
    connection_category: str

    # column is relationship name eg 'Relates To'

    @property
    def _filter_str(self) -> str:
        return f'{self.column}, {self.connection_category}, "{self.value}"'


class ConnectedFieldFilter(ConnectedItemFilter):
    kind: Literal['CTCF'] = 'CTCF'
    connected_column: str

    @classmethod
    def from_fil(cls, field_fil: CmcFilter, connection: Connection2):
        return cls.model_validate(
            cls(
                column=connection.name,
                connection_category=connection.category,
                connected_column=field_fil.column,
                condition=field_fil.condition,
                value=field_fil.value,
            )
        )

    @property
    def _filter_str(self):
        return f'{self.column}, {self.connection_category}, {self.connected_column}, {self.condition}, "{self.value}"'


class ConnectedItemConnectedItemFilter(ConnectedFieldFilter):
    kind: Literal['CTCTI'] = 'CTCTI'
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
    logics: list[Logic] = Field(default_factory=list)

    def __bool__(self):
        return bool(self.filters)

    # noinspection PyTypeChecker
    @model_validator(mode='after')
    def val_logics(self):
        if not self.logics:
            self.logics = ['And'] * (len(self.filters) - 1)
        if not len(self.logics) == len(self.filters) - 1:
            logger.warning(f'{self.logics=}, {self.filters=}')
            # raise ValueError('Logics must be one less than filters')
        return self

    def __add__(self, other: FilterArray):
        if not all([self, other]):
            return self if self else other
        return self.add_filters(*other.filters.values())

    def __str__(self):
        return f'{len(self.filters)} Filters:{'\n'.join(self.filter_strs)}\nSorted by {self.view_sort_text} Logic={self.sort_logics_text}'

    @property
    def sorts_txt(self):
        return ', '.join([f'{col}, {order.value}' for col, order in self.sorts])

    @property
    def view_sort_text(self):
        return f'[ViewSort({self.sorts_txt})]'

    @property
    def sort_logics_text(self):
        return f'[ViewConjunction({' ,'.join(self.logics)})]'

    @property
    def filter_strs(self):
        return [fil.view_filter_str(slot) for slot, fil in self.filters.items()]

    def update(self, pkg: dict):
        self.filters.update(pkg)

    def add_filter(self, cmc_filter: FieldFilter, logic: Logic = 'And'):
        lenn = len(self.filters)
        if lenn > 8:
            raise ValueError('No empty slots available')
        logger.debug(f'Adding filter {cmc_filter} to slot {lenn + 1}')
        self.filters[lenn + 1] = cmc_filter
        if lenn > 0:
            logger.debug(f'Adding logic {logic} between slots {lenn} and {lenn + 1}')
            self.logics.append(logic)

    def add_filters(self, *filters: tuple[FieldFilter, Logic]):
        for cmcfilter in filters:
            self.add_filter(*cmcfilter)

    @classmethod
    def from_filters(cls, *filters: FieldFilter, sorts=None, logics: list[Logic] = None):
        logics = logics or []
        sorts = sorts or ()
        filters_ = {i: fil for i, fil in enumerate(list(filters), 1)}
        return cls(filters=filters_, logics=logics, sorts=sorts)


def field_fil_to_confil(field_fil: FieldFilter, connection: Connection2):
    hireconfil = ConnectedFieldFilter(
        column=connection.name,
        connection_category=connection.category,
        connected_column=field_fil.column,
        condition=field_fil.condition,
        value=field_fil.value,
    )
    return hireconfil.model_validate(hireconfil, from_attributes=True)
