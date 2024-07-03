from __future__ import annotations

import contextlib
from functools import cached_property
from typing import Self
from collections.abc import Generator

from loguru import logger

from .pycmc_types import Connection2, CursorType
from .filters import CmcFilter, FilterArray
from .wrapper.cursor_wrapper import CursorWrapper
from .exceptions import PyCommenceExistsError, raise_for_one


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
    @cached_property
    def headers(self):
        """Column labels."""
        return self.cursor_wrapper.get_query_row_set(1).headers

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
            rs = self.cursor_wrapper.get_query_row_set(2)
            raise_for_one(rs)
            return rs.get_row_id(0)

    def pk_to_row_ids(self, pk: str) -> list[str]:
        with self.temporary_filter_by_array(self.pk_filter(pk)):
            rs = self.cursor_wrapper.get_query_row_set()
            return [rs.get_row_id(i) for i in range(rs.row_count)]

    def row_id_to_pk(self, row_id: str) -> str:
        """Convert row ID to primary key."""
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.get_value(0, 0)

    # row operations by id
    def read_row_by_id(self, row_id: str) -> dict[str, str]:
        rs = self.cursor_wrapper.get_query_row_set_by_id(row_id)
        return rs.row_dicts_list()[0]

    def update_row_by_id(self, row_id, update_pkg: dict):
        rs = self.cursor_wrapper.get_edit_row_set_by_id(row_id)
        rs.modify_row(0, update_pkg)
        assert rs.commit()

    def delete_row_by_id(self, row_id: str) -> None:
        rs = self.cursor_wrapper.get_delete_row_set_by_id(row_id)
        rs.delete_row(0)
        assert rs.commit()

    # row operations by pk
    def create_row_by_pkg(self, create_pkg: dict[str, str]) -> None:
        pkg_pk = create_pkg.get(self.pk_label)
        if not pkg_pk:
            raise ValueError(f'Primary key {self.pk_label} not provided in create_pkg.')
        if self.pk_exists(pkg_pk):
            raise PyCommenceExistsError(f'Primary key {pkg_pk} already exists.')
        rs = self.cursor_wrapper.get_add_row_set(count=1)
        rs.modify_row(0, create_pkg)
        rs.commit()

    def read_row_by_pk(self, pk: str) -> dict[str, str]:
        with self.temporary_filter_by_array(self.pk_filter(pk)):
            rs = self.cursor_wrapper.get_query_row_set(1)
            raise_for_one(rs)
            return rs.row_dicts_list()[0]

    def update_row_by_pk(self, pk, update_pkg: dict):
        row_id = self.pk_to_row_id(pk)
        self.update_row_by_id(row_id, update_pkg)

    def delete_row_by_pk(self, pk: str) -> None:
        row_id = self.pk_to_row_id(pk)
        self.delete_row_by_id(row_id)

    def rows(self, count: int | None = None, with_id: bool = False, with_category: bool = False) -> Generator[
        dict[str, str], None, None]:
        """Return all or first `count` records from the cursor."""
        row_set = self.cursor_wrapper.get_query_row_set(count)
        for row in row_set.row_dicts_gen(with_id=with_id):
            if with_category:
                row.update({'category': self.category})
            logger.debug(f'yielding {self.category} row {row.get(self.pk_label), ''}')
            yield row

    # row operations by filter
    def rows_by_filter(self, filter_array: FilterArray, count: int | None = None, with_id: bool = False) -> Generator[
        dict[str, str], None, None]:
        """Return all or first `count` records from the cursor."""
        with self.temporary_filter_by_array(filter_array):
            yield from self.rows(count, with_id)

    # filter operations
    def filter_by_array(self, filter_array: FilterArray | None = None) -> Self:
        """Enable the filter array."""
        filter_array = filter_array or self.filter_array
        [self.cursor_wrapper.set_filter(filstr) for filstr in filter_array.filter_strs]
        if filter_array.sorts:
            sort_text = f'[ViewSort({filter_array.sorts_txt})]'
            self.cursor_wrapper.set_sort(sort_text)
        if filter_array.logic:
            self.cursor_wrapper.set_filter_logic(filter_array.logic)
        return self

    @contextlib.contextmanager
    def temporary_filter_by_array(self, fil_array: FilterArray | None = None):
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

    def add_related_column(self, connection: Connection2) -> Self:
        """Add a related column to the cursor."""
        res = self.cursor_wrapper.set_related_column(
            col=self.column_count + 1,
            con_name=connection.name,
            connected_cat=connection.category,
            col_name=connection.column
        )
        if not res:
            raise ValueError('Failed to add related column.')
        return self
