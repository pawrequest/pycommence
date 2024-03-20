from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, TYPE_CHECKING

from pydantic import BaseModel, Field, model_validator

if TYPE_CHECKING:
    from pycommence import Csr

FilterConditionType = Literal['Equal To', 'Contains', 'After']
FilterType = Literal['F', 'CTI', 'CTCF', 'CTCTI']

NotFlagType = Literal['Not', '']


class FilterArray(BaseModel):
    filters: dict[int, CmcFilter] = Field(default_factory=dict)

    def add_filters(self, *filters: CmcFilter):
        for i, fil in enumerate(filters):
            self.filters[i + 1] = fil
        return self

    def filter_csr(self, csr: Csr):
        for slot, fil in self.filters.items():
            fil.filter_csr(csr, slot)


class CmcFilter(BaseModel):
    cmc_col: str
    condition: FilterConditionType = 'Equal To'
    value: str = ""
    f_type: FilterType = 'F'
    not_flag: NotFlagType = ''

    @model_validator(mode="after")
    def condition_val(self):
        if self.condition == 'Contains' or self.condition == 'Equal To':
            if not self.value:
                raise ValueError('Value must be set when condition is "Contains"')
        self.value = f', "{self.value}"' if self.value else ""

    def filter_str(self, slot: int) -> str:
        filter_str = (
            f"[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self.cmc_col}, {self.condition}{self.value})]"
        )
        return filter_str

    def filter_csr(self, csr: Csr, slot: int = 1):
        csr.filter_by_cmcfil(self, slot)
        return self


@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


class CmcError(Exception):
    def __init__(self, msg="Commence is not installed"):
        self.msg = msg
        super().__init__(self.msg)


CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def get_cmc_date(datestr: str):
    """ Use CMC Cannonical flag"""
    return datetime.strptime(datestr, CmcDateFormat).date()


def get_cmc_time(time_str: str):
    """ Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()
