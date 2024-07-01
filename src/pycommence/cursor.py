from __future__ import annotations

import contextlib
from typing import Self

from comtypes import CoInitialize, CoUninitialize

from pycommence.wrapper import rowset
from .exceptions import PyCommenceMaxExceededError, PyCommenceNotFoundError
from .pycmc_types import CmcFilter, ConditionType, Connection, FilterArray, NoneFoundHandler
from .wrapper.cmc_csr import CursorWrapper
from .wrapper.cmc_db import CommenceWrapper
from .wrapper.enums_cmc import CursorType


@contextlib.contextmanager
def csr_context(table_name, cmc_name: str = 'Commence.DB', filter_array: FilterArray | None = None) -> CursorAPI:
    """Context manager for :class:`Csr`. pywincom handles teardown afaik."""
    CoInitialize()
    try:
        csr_api = get_csr(table_name, cmc_name)
        if filter_array:
            csr_api.filter_by_array(filter_array)
        yield csr_api
    finally:
        CoUninitialize()


def get_csr(
    table_name,
    cmc_name: str = 'Commence.DB',
    mode: CursorType = CursorType.CATEGORY,
) -> CursorAPI:
    """Get Csr via (cached)  :class:`~pycommence.wrapper.cmc_db.Cmc`. instance."""
    cmc = CommenceWrapper(cmc_name)
    csr_cmc = cmc.get_new_cursor(table_name, mode=mode)
    return CursorAPI(csr_cmc, db_name=cmc.name)


class CursorAPI:
    """Commence Cursor object.

    Provides access to rowsets and filter methods
    """

    def __init__(
        self,
        cursor_wrapper: CursorWrapper,
        db_name: str,
        mode: CursorType = CursorType.CATEGORY,
        name: str = '',
        filter_array: FilterArray | None = None,
    ):
        self.cursor_wrapper = cursor_wrapper
        self.db_name = db_name
        self.mode = mode
        self.name = name
        self.filter_array = filter_array

    def enable_filter_array(self):
        """Enable the filter array."""
        self.filter_by_array(self.filter_array)

    def disable_filter_array(self):
        """Disable the filter array."""
        self.clear_all_filters()

    # @property
    # def table_name(self):
    #     return self.cursor_wrapper.

    def get_add_rowset(self, count: int = 1) -> rowset.RowSetAdd:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_add_row_set`."""
        return self.cursor_wrapper.get_add_row_set(count=count)

    def get_edit_rowset(self, count: int = 1) -> rowset.RowSetEdit:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_edit_row_set`."""
        return self.cursor_wrapper.get_edit_row_set(count=count)

    def get_delete_rowset(self, count: int = 1) -> rowset.RowSetDelete:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_delete_row_set`."""
        return self.cursor_wrapper.get_delete_row_set(count=count)

    def get_query_rowset(self, count: int | None = None) -> rowset.RowSetQuery:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_query_row_set`."""

        return self.cursor_wrapper.get_query_row_set(count=count)

    def get_named_addset(self, pk_val: str) -> rowset.RowSetAdd:
        """Get an add rowset and set the primary key value."""
        row_set = self.get_add_rowset()
        row_set.modify_row(0, 0, pk_val)
        return row_set

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
            self.filter_by_pk(pk, fslot=slot, none_found=none_found)
            filtered = True
            yield
        finally:
            if filtered:
                self.clear_filter(slot)

    def pk_exists(self, pk: str) -> bool:
        """Check if primary key exists in the Cursor."""
        with self.temporary_filter_pk(pk, none_found=NoneFoundHandler.ignore):
            return self.row_count > 0

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

    @property
    def pk_label(self):
        """Primary key label."""
        qs = self.cursor_wrapper.get_query_row_set(1)
        pk_label = qs.get_column_label(0)
        return pk_label

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

    def filter_by_connection(self, item_name: str, connection: Connection, *, fslot=1) -> None:
        """Filter by connection.

        Args:
            item_name: Item name
            connection: Connection object
            fslot: Filter slot

        """
        filter_str = f'[ViewFilter({fslot}, CTI,, {connection.name}, ' f'{connection.to_table}, {item_name})]'
        self.cursor_wrapper.set_filter(filter_str)

    def set_filter(self, cmc_filter: CmcFilter, slot=1) -> None:
        """Filter by CmcFilter object

        Args:
            cmc_filter: CmcFilter object
            slot: Filter slot

        """
        self.filter_by_str(cmc_filter.filter_str2(slot))

    def filter_by_array(self, fil_array: FilterArray) -> Self:
        """Filter by FilterArray object

        Args:
            fil_array: FilterArray object

        """
        for slot, fil in fil_array.filters.items():
            self.set_filter(fil, slot)
        return self

    def filter_by_str(self, filter_str: str) -> None:
        """Filter by commence-style filter string."""
        self.cursor_wrapper.set_filter(filter_str)

    def clear_filter(self, slot=1) -> None:
        self.filter_by_str(f'[ViewFilter({slot},Clear)]')

    def clear_all_filters(self) -> None:
        """Clear all filters."""
        [self.clear_filter(i) for i in range(1, 9)]

    def filter_by_pk(
        self,
        pk: str,
        *,
        fslot=1,
        none_found: NoneFoundHandler = NoneFoundHandler.error,
        max_return: int = 1,
    ):
        """Filter by primary key.

        Args:
            pk: Primary key value
            fslot: Filter slot
            none_found: What to do if no record is found
            max_return: Maximum number of records to return

        """
        filter_array = FilterArray(
            filters={fslot: CmcFilter(cmc_col=self.pk_label, condition=ConditionType.EQUAL, value=pk)}
        )
        self.filter_by_array(filter_array)
        count = self.row_count
        if count == 0:
            if none_found == 'error':
                raise PyCommenceNotFoundError(f'No record found for {self.pk_label} {pk}')
        if count > max_return:
            raise PyCommenceMaxExceededError(f'Expected max {max_return} record/s, got {count}')
