"""
API for Commence Cursor objects.
provides access to the Commence Cursor object and methods to interact with it.

"""
from __future__ import annotations

import typing as _t
import contextlib
from functools import cached_property
from typing import TYPE_CHECKING

from loguru import logger

from .db_api import Cmc
from .types_api import CmcError, CmcFilter, Connection, FilterArray

if TYPE_CHECKING:
    from pycommence.wrapper.cursor import CsrCmc


@contextlib.contextmanager
def csr_context(table_name, cmc_name: str = 'Commence.DB') -> Csr:
    """Access Commence DB via Csr object context-manager."""
    try:
        csr_api = get_csr(table_name, cmc_name)
        yield csr_api
    finally:
        ...


def get_csr(table_name, cmc_name: str = 'Commence.DB') -> Csr:
    """Create cached connection to Commence and return a Csr to operate on it."""
    cmc = Cmc(cmc_name)
    csr_cmc = cmc.get_cursor(table_name)
    csr_api = Csr(csr_cmc)
    return csr_api


# def num_matches(table, k: str, v: str) -> bool:
#     with csr_context(table) as csr:
#         csr.filter_by_field(k, 'Equal To', v)
#         return csr.row_count


class Csr:
    def __init__(self, cursor: CsrCmc):
        self._cursor_cmc = cursor

    @property
    def category(self):
        return self._cursor_cmc.category

    @property
    def column_count(self):
        return self._cursor_cmc.column_count

    @property
    def row_count(self):
        return self._cursor_cmc.row_count

    @property
    def shared(self):
        return self._cursor_cmc.shared

    @cached_property
    def pk_label(self):
        qs = self._cursor_cmc.get_query_row_set(1)
        return qs.get_column_label(0)

    def records(self, count: int or None = None) -> list[dict[str, str]]:
        row_set = self._cursor_cmc.get_query_row_set(count)
        records = row_set.get_rows_dict()
        return records

    def one_record(self, pk_val: str) -> dict[str, str]:
        self.filter_by_pk(pk_val)
        return self.records(1)[0]

    def records_by_field(
            self, field_name: str,
            value: str,
            max_rtn=None,
            empty: _t.Literal['ignore', 'raise'] = 'raise'
    ) -> list[dict[str, str]]:
        """
        Get records from the cursor by field name and value.

        Args:
            field_name: Name of the field to query.
            value: Value to filter by.
            max_rtn: Maximum number of records to return. If more than this, raise CmcError.

        Returns:
            A list of dictionaries of field names and values for the record.

        Raises:
            CmcError: If the record is not found or if more than max_rtn records are found.

        """
        self.filter_by_field(field_name, 'Equal To', value)
        records = self.records()
        if not records and empty == 'raise':
            raise CmcError(f'No record found for {field_name} {value}')
        if max_rtn and len(records) > max_rtn:
            raise CmcError(f'Expected max {max_rtn} records, got {len(records)}')
        return records

    def edit_record(
            self,
            pk_val: str,
            package: dict,
    ) -> bool:
        """Modify a record in the cursor and commit.

        Args:
            pk_val (str): The value for the primary key field.
            package (dict): A dictionary of field names and values to modify.
            multiple (str): Action to take if more than one record is found. Options are 'raise'.

        Returns:
            bool: True on success

            """
        self.filter_by_pk(pk_val)
        row_set = self._cursor_cmc.get_edit_row_set()
        row_set.modify_row_dict(0, package)
        return row_set.commit()

    def delete_record_by_pk(self, pk_val: str):
        self.filter_by_pk(pk_val)
        if self.row_count > 1:
            raise CmcError(f'Expected max 1 records, got {self.row_count}')
        row_set = self._cursor_cmc.get_delete_row_set()
        row_set.delete_row(0)
        return row_set.commit()

    def add_record(
            self,
            pk_val: str,
            package: dict,
            existing: _t.Literal['replace', 'update', 'raise'] = 'raise'
    ) -> bool:
        """
        Add and commit a record to the cursor.

        Args:
            pk_val: The value for the primary key field.
            package: A dictionary of field names and values to add to the record.
            existing: Action to take if the record already exists. Options are 'replace', 'update', 'raise'.

        Returns:
            bool: True on success
            """
        self.filter_by_pk(pk_val, empty='ignore')
        if self.row_count == 1:
            match existing:
                case 'raise':
                    raise CmcError('Record already exists')
                case 'replace':
                    self.delete_record_by_pk(pk_val)
                case 'update':
                    return self.edit_record(pk_val, package)

        add_set = self._cursor_cmc.get_add_row_set(1)
        add_set.modify_row(0, 0, pk_val)
        add_set.modify_row_dict(0, package)
        if not add_set.get_value(0, 0):
            raise CmcError('Column0 must be set')
        res = add_set.commit()
        return res

        # try:
        # except com_error as e:
        #     # todo this is horrible. the error is related to threading but we are not using threading?
        #     # maybe pywin32 uses threading when handling the underlying db error?
        #     if e.hresult == -2147483617:
        #         raise CmcError('Record already exists')
        #     raise

    def filter_by_field(
            self,
            field_name: str,
            condition: str,
            value: str = '',
            *,
            get=False,
            fslot: int = 1
    ) -> None | list[dict[str, str]]:
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        self._cursor_cmc.set_filter(filter_str)
        if get:
            return self.records()

    def filter_by_connection(
            self,
            item_name: str,
            connection: Connection,
            *,
            get=False,
            fslot=1
    ) -> None | list[dict[str, str]]:
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        self._cursor_cmc.set_filter(filter_str)
        if get:
            return self.records()

    def filter_by_cmcfil(self, cmc_filter: CmcFilter, slot=1, *, get=False) -> None | list[
        dict[str, str]]:
        self.filter_by_str(cmc_filter.filter_str(slot))
        if get:
            return self.records()

    def filter_by_array(self, fil_array: FilterArray, get=False) -> None | list[dict[str, str]]:
        for slot, fil in fil_array.filters.items():
            self.filter_by_cmcfil(fil, slot)
        if get:
            return self.records()

    def filter_by_str(self, filter_str: str):
        """ commence syntax filter string"""
        self._cursor_cmc.set_filter(filter_str)

    def clear_filter(self, slot=1):
        self.filter_by_str(f'[ViewFilter({slot},Clear)]')

    def filter_by_pk(self, pk: str, *, fslot=1, empty: _t.Literal['raise', 'ignore'] = 'raise'):
        self.filter_by_field(self.pk_label, 'Equal To', value=pk, fslot=fslot)
        if self.row_count == 0:
            if empty == 'raise':
                raise CmcError(f'No record found for {self.pk_label} {pk}')
        if self.row_count > 1:
            raise CmcError(f'Expected 1 record, got {self.row_count}')

    # def set_filters(self, filters: list[CmcFilter], get_all=False):
    #     for i, fil in enumerate(filters, start=1):
    #         self.filter_by_cmcfil(fil, i)
    #     if get_all:
    #         return self.get_records()
