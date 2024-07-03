from __future__ import annotations

import contextlib
from typing import Self

from pycommence.wrapper import rowset
from .pycmc_types import CmcFilter, FilterArray, NoneFoundHandler
from .wrapper.cmc_csr import CursorWrapper
from .wrapper.enums_cmc import CursorType


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

    @property
    def category(self):
        """Commence Category name."""
        return self.cursor_wrapper.category

    def filter_by_array(self, filter_array: FilterArray | None = None) -> Self:
        """Enable the filter array."""
        filter_array = filter_array or self.filter_array
        filter_wrapper_by_array(self.cursor_wrapper, filter_array)
        return self

    def get_row_by_id(self, row_id: str) -> rowset.RowSetQuery:
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.get_row(0)

    def delete_row_by_id(self, row_id: str) -> None:
        rs = self.cursor_wrapper.get_delete_row_set_by_id(row_id)
        rs.delete_row(0)
        assert rs.commit()

    def edit_row_by_id(self, row_id, update_pkg: dict):
        rs = self.cursor_wrapper.get_edit_row_set_by_id(row_id)
        rs.modify_row(0, **update_pkg)
        assert rs.commit()

    @contextlib.contextmanager
    def temporary_filter_pk(self, pk: str, *, slot: int = 4, none_found: NoneFoundHandler = NoneFoundHandler.error):
        """Temporarily filter by primary key.

        Args:
            pk: Primary key value
            slot: Filter slot
            none_found: What to do if no record is found

        """
        filtered = False
        try:
            self.filter_by_pk(pk)
            filtered = True
            yield
        finally:
            if filtered:
                self.clear_filter(slot)

    def pk_exists(self, pk: str) -> bool:
        """Check if primary key exists in the Cursor."""
        with self.temporary_filter_pk(pk):
            if self.row_count > 1:
                raise ValueError(f'Multiple records found for primary key {pk}')
            return self.row_count == 1

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

    @property
    def pk_label(self):
        """Primary key label."""
        qs = self.cursor_wrapper.get_query_row_set(1)
        pk_label = qs.get_column_label(0)
        return pk_label

    def pk_to_row_id(self, pk: str) -> str:
        """Convert primary key to row ID."""
        with self.temporary_filter_pk(pk):
            assert self.row_count == 1
            rs = self.cursor_wrapper.get_query_row_set(1)
            return rs.get_row_id(0)

    def row_id_to_pk(self, row_id: str) -> str:
        """Convert row ID to primary key."""
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.get_value(0, 0)

    def filter_by_pk(self, pk: str):
        return self.filter_by_array(FilterArray.from_filters(CmcFilter(cmc_col=self.pk_label, value=pk)))

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
