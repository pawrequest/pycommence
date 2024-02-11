from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FilterCondition(StrEnum):
    EQUAL_TO = "Equal To"
    CONTAINS = "Contains"
    AFTER = "After"


class FilterType(StrEnum):
    FIELD = 'F'
    CONNECTION = 'CTI'
    CATEGORY = 'CTCF'
    CATEGORY_ITEM = 'CTCTI'


class NotFlag(StrEnum):
    NOT = 'Not'
    BLANK = ''


@dataclass
class CmcFilter:
    """
    ViewFilter
    Syntax: [ViewFilter(ClauseNumber, FilterType, NotFlag, FilterTypeParameters)]
    Request Item for the ViewData topic
    Defines the criteria for the multiple filter to be applied against the previously named category (see ViewCategory).
    ClauseNumber defines which filter clause is being defined, where ClauseNumber is between 1 and 4.
    FilterType sets the type of the filter to apply.
    NotFlag determines if a logical Not is applied against the entire clause. The NotFlag parameter must be specified; it may be either Not or left blank (by specifying the comma placeholder for that parameter). This is equivalent to the "Except" checkbox found in the Commence filter dialog boxes.
    The FilterTypeParameters specified with this REQUEST and the ViewConjunction REQUEST are similar to those available from the Commence main menu.
    """

    field_name: str
    condition: FilterCondition = FilterCondition.EQUAL_TO
    value: str = ''
    f_type: FilterType = FilterType.FIELD
    not_flag: NotFlag = NotFlag.BLANK
    slot: int = 1

    def __post_init__(self):
        if self.condition == FilterCondition.CONTAINS or self.condition == FilterCondition.EQUAL_TO:
            if not self.value:
                raise ValueError('Value must be set when condition is "Contains"')
        self.value = f', "{self.value}"' if self.value else ''

    @property
    def filter_str(self) -> str:
        filter_str = f'[ViewFilter({self.slot}, {self.f_type}, {self.not_flag}, {self.field_name}, {self.condition}{self.value})]'
        return filter_str
