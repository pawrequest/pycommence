from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple

from pycommence.meta.meta import CommenceTable


@dataclass
class RowData(NamedTuple):
    category: str
    row_id: str
    data: dict[str, str]


@dataclass
class CommenceRecord[T:CommenceTable]:
    table: T
    row_data: RowData
    context: dict[str, str] = field(default_factory=dict)
