from __future__ import annotations

import contextlib
from collections.abc import Generator
from functools import cached_property
from typing import Self

from .exceptions import PyCommenceExistsError, raise_for_one
from .filters import ConditionType, FieldFilter, FilterArray
from .pycmc_types import Connection, CursorType, MoreAvailable, Pagination, RowFilter, SeekBookmark
from .wrapper.cursor_wrapper import CursorWrapper


def raise_for_id_or_pk(id, pk):
    if not any([id, pk]):
        raise ValueError('Must provide id or pk')


class CursorAPI:
    def __init__(
        self,
        cursor_wrapper: CursorWrapper,
        mode: CursorType = CursorType.CATEGORY,
        csrname: str = '',
    ):
        self.cursor_wrapper = cursor_wrapper
        self.mode = mode
        self.csrname = csrname

    # proxied from wrapper
    # @cached_property
    # def headers(self):
    #     """Column labels."""
    #     return self.cursor_wrapper.get_query_row_set(1).headers

    @property
    def category(self) -> str:
        """Commence Category name."""
        return self.cursor_wrapper.category

    @property
    def column_count(self) -> int:
        """Number of columns in the Cursor."""
        return self.cursor_wrapper.column_count

    @property
    def row_count(self) -> int:
        """Number of rows in the Cursor."""
        return self.cursor_wrapper.row_count

    @property
    def shared(self) -> bool:
        """True if the database is enrolled in a workgroup."""
        return self.cursor_wrapper.shared

    # pk operations
    @cached_property
    def pk_label(self) -> str:
        """Column 0 label."""
        rs = self.cursor_wrapper.get_query_row_set(0)
        return rs.get_column_label(0)

    def pk_filter(self, pk, condition=ConditionType.EQUAL) -> FieldFilter:
        return FieldFilter(column=self.pk_label, condition=condition, value=pk)

    def pk_exists(self, pk: str) -> bool:
        """Check if primary key exists in the Cursor."""
        with self.temporary_filter(FilterArray.from_filters(self.pk_filter(pk))):
            return self.row_count > 0

    def pk_to_id(self, pk: str) -> str:
        """Convert primary key to row ID."""
        with self.temporary_filter(FilterArray.from_filters(self.pk_filter(pk))):
            with self.temporary_offset(0):
                rs = self.cursor_wrapper.get_query_row_set(2)
                raise_for_one(rs)
                return rs.get_row_id(0)

    def pk_to_row_ids(self, pk: str) -> list[str]:
        with self.temporary_filter(FilterArray.from_filters(self.pk_filter(pk))):
            with self.temporary_offset(0):
                rs = self.cursor_wrapper.get_query_row_set()
                return [rs.get_row_id(i) for i in range(rs.row_count)]

    def row_id_to_pk(self, row_id: str) -> str:
        """Convert row ID to primary key."""
        with self.temporary_offset(0):
            rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
            return rs.get_value(0, 0)

    # CREATE
    def _create_row(self, create_pkg: dict[str, str]) -> None:
        pkg_pk = create_pkg.get(self.pk_label)
        if not pkg_pk:
            raise ValueError(f'Primary key {self.pk_label} not provided in create_pkg.')
        if self.pk_exists(pkg_pk):
            raise PyCommenceExistsError(f'Primary key {pkg_pk} already exists.')
        rs = self.cursor_wrapper.get_add_row_set(limit=1)
        rs.modify_row(0, create_pkg)
        rs.commit()

    # READ
    def _read_row(
        self, *, row_id: str | None = None, pk: str | None = None, with_category: bool = False
    ) -> dict[str, str]:
        raise_for_id_or_pk(row_id, pk)
        with self.temporary_offset(0):
            row_id = row_id or self.pk_to_id(pk)
            rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
            raise_for_one(rs)
            row = next(rs.rows())
            row['row_id'] = row_id
            if with_category:
                self.add_category_to_dict(row)
            return row

    def _read_rows(
        self,
        pagination: Pagination | None = None,
        filter_array: FilterArray | None = None,
        row_filter: RowFilter | None = None,
    ) -> Generator[dict[str, str] | MoreAvailable, None, None]:
        pagination = pagination or Pagination()
        filter_manager = self.temporary_filter(filter_array) if filter_array else contextlib.nullcontext()
        offset_manager = self.temporary_offset(pagination.offset)
        with offset_manager, filter_manager:
            rowset = self.cursor_wrapper.get_query_row_set(pagination.limit)
            rowgen = rowset.rows()
            rowgen = row_filter(rowgen) if row_filter else rowgen
            for i, row in enumerate(rowgen, start=1):
                if i > pagination.limit:
                    break
                self.add_category_to_dict(row)
                yield row

    # UPDATE
    def _update_row(self, update_pkg: dict, *, id: str | None = None, pk: str | None = None):
        raise_for_id_or_pk(id, pk)
        id = id or self.pk_to_id(pk)
        rs = self.cursor_wrapper.get_edit_row_set_by_id(id)
        rs.modify_row(0, update_pkg)
        assert rs.commit()

    # DELETE
    def _delete_row(self, id: str | None = None, pk: str | None = None) -> None:
        raise_for_id_or_pk(id, pk)
        id = id or self.pk_to_id(pk)
        rs = self.cursor_wrapper.get_delete_row_set_by_id(id)
        rs.delete_row(0)
        assert rs.commit()

    def add_category_to_dict(self, row):
        row.update({'category': self.category})

    # FILTER
    def filter_by_array(self, filter_array: FilterArray) -> Self:
        [self.cursor_wrapper.set_filter(filstr) for filstr in filter_array.filter_strs]
        if filter_array.sorts:
            self.cursor_wrapper.set_sort(filter_array.view_sort_text)
        if filter_array.logics:
            self.cursor_wrapper.set_filter_logic(filter_array.sort_logics_text)
        return self

    @contextlib.contextmanager
    def temporary_offset(self, offset: int):
        """Temporarily offset the cursor."""
        try:
            self.cursor_wrapper.seek_row(SeekBookmark.CURRENT, offset)
            yield
        finally:
            self.cursor_wrapper.seek_row(SeekBookmark.BEGINNING, 0)

    @contextlib.contextmanager
    def temporary_filter(self, fil_array: FilterArray):
        """Temporarily filter by FilterArray object.

        Args:
            fil_array: FilterArray object

        """
        try:
            self.clear_all_filters()
            self.filter_by_array(fil_array)
            yield
        finally:
            self.clear_all_filters()

    def clear_filter(self, slot=1) -> None:
        self.cursor_wrapper.set_filter(f'[ViewFilter({slot},Clear)]')

    def clear_all_filters(self) -> None:
        """Clear all filters."""
        [self.clear_filter(i) for i in range(1, 9)]

    def add_related_column(self, connection: Connection) -> Self:
        """Add a related column to the cursor."""
        res = self.cursor_wrapper.set_related_column(
            col=self.column_count + 1,
            con_name=connection.name,
            connected_cat=connection.category,
            col_name=connection.column,
        )
        if not res:
            raise ValueError('Failed to add related column.')
        return self
