from __future__ import annotations

import contextlib
from functools import cached_property

from comtypes import CoInitialize, CoUninitialize
from loguru import logger

from .pycmc_types import CmcError, CmcFilter, Connection, FilterArray, NoneFoundHandler
from pycommence.wrapper import rowset
from .wrapper.cmc_csr import CursorWrapper
from .wrapper.cmc_db import CommenceWrapper


@contextlib.contextmanager
def csr_context(table_name, cmc_name: str = 'Commence.DB') -> CursorAPI:
    """Context manager for :class:`Csr`. pywincom handles teardown afaik."""
    CoInitialize()
    try:
        csr_api = get_csr(table_name, cmc_name)
        yield csr_api
    finally:
        CoUninitialize()


def get_csr(table_name, cmc_name: str = 'Commence.DB') -> CursorAPI:
    """Get Csr via (cached)  :class:`~pycommence.wrapper.cmc_db.Cmc`. instance."""
    cmc = CommenceWrapper(cmc_name)
    csr_cmc = cmc.get_cursor(table_name)
    return CursorAPI(csr_cmc, db_name=cmc.name)


class CursorAPI:
    """Commence Cursor object.

    Provides access to rowsets and filter methods
    """

    def __init__(self, csr_cmc: CursorWrapper, db_name: str):
        self.cursor_wrapper = csr_cmc
        self.db_name = db_name

    def get_add_rowset(self, count: int = 1) -> rowset.RowSetAdd:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_add_row_set`."""
        return self.cursor_wrapper.get_add_row_set(count=count)

    def get_edit_rowset(self, count: int = 1) -> rowset.RowSetEdit:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_edit_row_set`."""
        return self.cursor_wrapper.get_edit_row_set(count=count)

    def get_delete_rowset(self, count: int = 1) -> rowset.RowSetDelete:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_delete_row_set`."""
        return self.cursor_wrapper.get_delete_row_set(count=count)

    def get_query_rowset(self, count: int = 1) -> rowset.RowSetQuery:
        """See :meth:`~pycommence.wrapper.cmc_csr.CsrCmc.get_query_row_set`."""

        return self.cursor_wrapper.get_query_row_set(count=count)

    def get_named_addset(self, pk_val: str) -> rowset.RowSetAdd:
        """Get an add rowset and set the primary key value."""
        row_set = self.get_add_rowset()
        row_set.modify_row(0, 0, pk_val)
        return row_set

    @contextlib.contextmanager
    def temporary_filter_pk(
            self,
            pk: str,
            *,
            slot: int = 4,
            none_found: NoneFoundHandler = NoneFoundHandler.error
    ):
        """Temporarily filter by primary key.

        Args:
            pk: Primary key value
            slot: Filter slot
            none_found: What to do if no record is found

        """
        try:
            self.filter_by_pk(pk, fslot=slot, none_found=none_found)
            yield
        finally:
            self.clear_filter(slot)

    @contextlib.contextmanager
    def temporary_filter_fields(
            self,
            field_key: str,
            condition: str,
            field_value: str,
            *,
            slot: int = 4,
            none_found: NoneFoundHandler = NoneFoundHandler.error

    ):
        """Temporarily filter by field.

        Args:
            field_key: Field name
            condition: Filter condition
            field_value: Value to filter by
            slot: Filter slot
            none_found: What to do if no record is found

        """
        try:
            self.filter_by_field(field_key, condition, field_value, fslot=slot, none_found=none_found)
            yield
        finally:
            self.clear_filter(slot)

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

    @cached_property
    def pk_label(self):
        """Primary key label."""
        qs = self.cursor_wrapper.get_query_row_set(1)
        return qs.get_column_label(0)

    def filter_by_field(
            self,
            field_name: str,
            condition: str,
            value: str = '',
            *,
            fslot: int = 1,
            none_found: NoneFoundHandler = NoneFoundHandler.error,
    ) -> bool:
        """Filter by field.

        Args:
            field_name: Field name
            condition: Filter condition
            value: Value to filter by
            fslot: Filter slot
            none_found: What to do if no record is found

        """
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        res = self.cursor_wrapper.set_filter(filter_str)
        if res:
            logger.debug(f'Filter set: {filter_str}')
        else:
            logger.info(f'Filter: {filter_str}')
            if none_found == NoneFoundHandler.error:
                raise CmcError(f'Error setting filter: {filter_str}')
        return res

    def filter_by_connection(
            self,
            item_name: str,
            connection: Connection,
            *,
            fslot=1
    ) -> None:
        """Filter by connection.

        Args:
            item_name: Item name
            connection: Connection object
            fslot: Filter slot

        """
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        self.cursor_wrapper.set_filter(filter_str)

    def filter_by_cmcfil(self, cmc_filter: CmcFilter, slot=1) -> None:
        """Filter by CmcFilter object

        Args:
            cmc_filter: CmcFilter object
            slot: Filter slot

        """
        self.filter_by_str(cmc_filter.filter_str(slot))

    def filter_by_array(self, fil_array: FilterArray) -> None:
        """Filter by FilterArray object

        Args:
            fil_array: FilterArray object

        """
        for slot, fil in fil_array.filters.items():
            self.filter_by_cmcfil(fil, slot)

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
            [self.clear_filter(slot=_) for _ in fil_array.filters.keys()]

    def filter_by_str(self, filter_str: str) -> None:
        """Filter by commence-style filter string."""
        self.cursor_wrapper.set_filter(filter_str)

    def clear_filter(self, slot=1) -> None:
        self.filter_by_str(f'[ViewFilter({slot},Clear)]')

    def filter_by_pk(
            self,
            pk: str,
            *,
            fslot=1,
            none_found: NoneFoundHandler = NoneFoundHandler.error
    ):
        """Filter by primary key.

        Args:
            pk: Primary key value
            fslot: Filter slot
            none_found: What to do if no record is found

        """
        if not pk:
            raise ValueError('pk must be a non-empty string')
        self.filter_by_field(
            self.pk_label,
            'Equal To',
            value=pk,
            fslot=fslot,
            none_found=none_found
        )
        if self.row_count == 0:
            if none_found == 'raise':
                raise CmcError(f'No record found for {self.pk_label} {pk}')
        if self.row_count > 1:
            raise CmcError(f'Expected 1 record, got {self.row_count}')
