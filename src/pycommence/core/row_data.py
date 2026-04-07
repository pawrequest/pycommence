from __future__ import annotations

import typing as _t
from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import NamedTuple

from pycommence.core.meta import CommenceTable, get_table_type
from pycommence.core.pagination import MoreAvailable


class RowInfo(NamedTuple):
    category: str
    row_id: str


@dataclass
class RowData:
    category: str
    row_id: str
    data: dict[str, str]
    _table_model_type: type[CommenceTable] | None = None

    @property
    def table_model(self) -> type[CommenceTable] | None:
        if not self._table_model_type:
            self._table_model_type = get_table_type(self.category, mode='all', missing='raise')
        return self._table_model_type

    def construct_model(self) -> CommenceTable:
        return self.table_model(row_id=self.row_id, **self.data)


RowFilter = Callable[[Generator[dict[str, str]]], Generator[dict[str, str]]]
RowDataGenerator = _t.Generator[RowData | MoreAvailable]
RowDataGeneratorAsync = _t.AsyncGenerator[RowData | MoreAvailable]
