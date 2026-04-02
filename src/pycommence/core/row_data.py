from __future__ import annotations

import typing as _t
from collections.abc import Callable, Generator
from dataclasses import dataclass

from loguru import logger

from pycommence.core.meta import CommenceTable, get_table_type
from pycommence.core.pagination import MoreAvailable


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

    def construct_model(self) -> CommenceTable | None:
        if table_type := self.table_model:
            return table_type.model_validate(self.data)
        logger.warning(f'No table model to construct: {self.category}')
        return None


RowFilter = Callable[[Generator[dict[str, str], None, None]], Generator[dict[str, str], None, None]]
RowDataGenerator = _t.Generator[RowData | MoreAvailable, None, None]
RowDataGeneratorAsync = _t.AsyncGenerator[RowData | MoreAvailable, None]
