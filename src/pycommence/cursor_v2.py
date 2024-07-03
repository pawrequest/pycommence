from __future__ import annotations

import contextlib
from functools import cached_property
from typing import Generator, Self

from .pycmc_types import CmcFilter, CursorType, FilterArray
from .wrapper.cursor_wrapper import CursorWrapper


class CursorAPI:
    def __init__(
        self,
        cursor_wrapper: CursorWrapper,
        mode: CursorType = CursorType.CATEGORY,
        csrname: str = '',
        filter_array: FilterArray | None = None,
    ):
        self.cursor_wrapper = cursor_wrapper
        self.mode = mode
        self.csrname = csrname
        self.filter_array = filter_array
        if self.filter_array:
            self.filter_by_array()

    # proxied from wrapper
    @property
    def category(self):
        """Commence Category name."""
        return self.cursor_wrapper.category

    @property
    def column_count(self):
        """Number of columns in the Cursor."""
        return self.cursor_wrapper.column_count

    @property
    def row_count(self):
        """Number of rows in the Cursor."""
        return self.cursor_wrapper.row_count

    @property
    def shared(self):
        """True if the database is enrolled in a workgroup."""
        return self.cursor_wrapper.shared

    # pk operations
    @cached_property
    def pk_label(self) -> str:
        """Column 0 label."""
        rs = self.cursor_wrapper.get_query_row_set(1)
        return rs.get_column_label(0)

    def pk_filter(self, pk):
        return FilterArray.from_filters(CmcFilter(cmc_col=self.pk_label, value=pk))

    def pk_exists(self, pk: str) -> bool:
        """Check if primary key exists in the Cursor."""
        with self.temporary_filter_by_array(self.pk_filter(pk)):
            return self.row_count > 0

    def pk_to_row_id(self, pk: str) -> str:
        """Convert primary key to row ID."""
        with self.temporary_filter_by_array(self.pk_filter(pk)):
            assert self.row_count == 1
            rs = self.cursor_wrapper.get_query_row_set(1)
            return rs.get_row_id(0)

    def row_id_to_pk(self, row_id: str) -> str:
        """Convert row ID to primary key."""
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.get_value(0, 0)

    # row operations
    def read_row_by_pk(self, pk: str) -> dict[str, str]:
        with self.temporary_filter_by_array(self.pk_filter(pk)):
            rs = self.cursor_wrapper.get_query_row_set(1)
            return rs.row_dicts_list()[0]

    def read_row_by_id(self, row_id: str) -> dict[str, str]:
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.row_dicts_list()[0]

    def delete_row_by_id(self, row_id: str) -> None:
        rs = self.cursor_wrapper.get_delete_row_set_by_id(row_id)
        rs.delete_row(0)
        assert rs.commit()

    def delete_row_by_pk(self, pk: str) -> None:
        row_id = self.pk_to_row_id(pk)
        self.delete_row_by_id(row_id)

    def update_row_by_id(self, row_id, update_pkg: dict):
        rs = self.cursor_wrapper.get_edit_row_set_by_id(row_id)
        rs.modify_row(0, **update_pkg)
        assert rs.commit()

    def update_row_by_pk(self, pk, update_pkg: dict):
        row_id = self.pk_to_row_id(pk)
        self.update_row_by_id(row_id, update_pkg)

    def rows(self, count: int | None = None, with_id: bool = False, with_category:bool = False) -> Generator[dict[str, str], None, None]:
        """Return all or first `count` records from the cursor."""
        row_set = self.cursor_wrapper.get_query_row_set(count)
        for row in row_set.row_dicts_gen(with_id=with_id):
            if with_category:
                row.update({'category': self.category})
            yield row

    # filter operations
    def filter_by_array(self, filter_array: FilterArray | None = None) -> Self:
        """Enable the filter array."""
        filter_array = filter_array or self.filter_array
        filter_wrapper_by_array(self.cursor_wrapper, filter_array)
        return self

    @contextlib.contextmanager
    def temporary_filter_by_array(self, fil_array: FilterArray):
        """Temporarily filter by FilterArray object.

        Args:
            fil_array: FilterArray object

        """
        try:
            self.filter_by_array(fil_array)
            yield
        finally:
            self.clear_all_filters()

    def clear_filter(self, slot=1) -> None:
        self.cursor_wrapper.set_filter(f'[ViewFilter({slot},Clear)]')

    def clear_all_filters(self) -> None:
        """Clear all filters."""
        [self.clear_filter(i) for i in range(1, 9)]


def filter_wrapper_by_array(csr_wrapper: CursorWrapper, filter_array: FilterArray) -> None:
    """Enable the filter array."""
    [csr_wrapper.set_filter(filstr) for filstr in filter_array.filter_strs]
    if filter_array.sortby:
        csr_wrapper.set_sort(filter_array.sortby)
    if filter_array.logic:
        csr_wrapper.set_filter_logic(filter_array.logic)
