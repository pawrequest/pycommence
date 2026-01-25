from __future__ import annotations

import dataclasses
from typing import NamedTuple


class RowInfo(NamedTuple):
    category: str
    id: str


class RowData(NamedTuple):
    row_info: RowInfo
    data: dict[str, str]

    @classmethod
    def from_data(cls, category: str, row_id: str, data: dict[str, str]) -> RowData:
        """Create a RowData instance from category, row_id, and data."""
        return cls(row_info=RowInfo(category=category, id=row_id), data=data)


@dataclasses.dataclass
class RowData2:
    category: str
    id: str
    data: dict[str, str]
