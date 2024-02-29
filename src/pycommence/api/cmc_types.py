from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum, Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, model_validator, Field

if TYPE_CHECKING:
    from pycommence.api import Csr


class FilterCondition(str, Enum):
    EQUAL_TO = "Equal To"
    CONTAINS = "Contains"
    AFTER = "After"


# FilterCondition = Literal['Equal To', 'Contains', 'After']
class FilterTypeEnum(StrEnum):
    FIELD = "F"
    CONNECTION = "CTI"
    CATEGORY = "CTCF"
    CATEGORY_ITEM = "CTCTI"


class NotFlag(StrEnum):
    NOT = "Not"
    BLANK = ""


class FilterArray(BaseModel):
    filters: dict[int, CmcFilter] = Field(default_factory=dict)

    def add_filters(self, *filters: CmcFilter):
        for i, fil in enumerate(filters):
            self.filters[i + 1] = fil
        return self

    def filter_csr(self, csr: Csr):
        for slot, filter in self.filters.items():
            filter.filter_csr(csr, slot)


class FilterArray1:
    def __init__(self, *filters):
        self.filters = {i + 1: filters[i] for i in range(len(filters))}


class CmcFilter(BaseModel):
    field_name: str
    condition: FilterCondition = FilterCondition.EQUAL_TO
    value: str = ""
    f_type: FilterTypeEnum = FilterTypeEnum.FIELD
    not_flag: NotFlag = NotFlag.BLANK

    @model_validator(mode="after")
    def condition(self):
        if self.condition == FilterCondition.CONTAINS or self.condition == FilterCondition.EQUAL_TO:
            if not self.value:
                raise ValueError('Value must be set when condition is "Contains"')
        self.value = f', "{self.value}"' if self.value else ""

    def filter_str(self, slot) -> str:
        filter_str = (
            f"[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self.field_name}, {self.condition}{self.value})]"
        )
        return filter_str

    def filter_csr(self, csr: Csr, slot: int = 1):
        csr.filter_py(self, slot)
        return self


# DEPREC DONT DELETE IN CASE!
# class CmcFilter:
#     """
#     ViewFilter
#     Syntax: [ViewFilter(ClauseNumber, FilterType, NotFlag, FilterTypeParameters)]
#     Request Item for the ViewData topic
#     Defines the criteria for the multiple filter to be applied against the previously named category (see ViewCategory).
#     ClauseNumber defines which filter clause is being defined, where ClauseNumber is between 1 and 4.
#     FilterType sets the type of the filter to apply.
#     NotFlag determines if a logical Not is applied against the entire clause. The NotFlag parameter must be specified; it may be either Not or left blank (by specifying the comma placeholder for that parameter). This is equivalent to the "Except" checkbox found in the Commence filter dialog boxes.
#     The FilterTypeParameters specified with this REQUEST and the ViewConjunction REQUEST are similar to those available from the Commence main menu.
#     """
#
#     def __init__(
#             self,
#             *,
#             field_name,
#             condition: FilterCondition = FilterCondition.EQUAL_TO,
#             value: str = '',
#             f_type: FilterTypeEnum = FilterTypeEnum.FIELD,
#             not_flag: NotFlag = NotFlag.BLANK
#     ):
#         self.field_name = field_name
#         self.condition = condition
#         self.f_type = f_type
#         self.not_flag = not_flag
#         self.value = value
#
#         if self.condition == FilterCondition.CONTAINS or self.condition == FilterCondition.EQUAL_TO:
#             if not self.value:
#                 raise ValueError('Value must be set when condition is "Contains"')
#         self.value = f', "{self.value}"' if self.value else ''
#
#     def filter_str(self, slot) -> str:
#         filter_str = f'[ViewFilter({slot}, {self.f_type}, {self.not_flag}, {self.field_name}, {self.condition}{self.value})]'
#         return filter_str
#
#     def filter_csr(self, csr: Csr, slot: int = 1):
#         csr.filter(self, slot)
@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


class CmcError(Exception):
    def __init__(self, msg="Commence is not installed"):
        self.msg = msg
        super().__init__(self.msg)


class NotFoundError(Exception):
    def __init__(self, msg="No records found"):
        self.msg = msg
        super().__init__(self.msg)
