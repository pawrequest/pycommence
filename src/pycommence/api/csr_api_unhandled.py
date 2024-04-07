"""
API for Commence Cursor objects.
provides access to the Commence Cursor object and methods to interact with it.

"""
from __future__ import annotations

import typing as _t
import contextlib
from functools import cached_property

from pycommence.api.db_api import Cmc
from pycommence.api import types_api
from pycommence.api.types_api import EmptyKind
from pycommence.wrapper.cursor import CsrCmc


@contextlib.contextmanager
def csr_context(table_name, cmc_name: str = 'Commence.DB') -> Csr:
    """Access Commence DB via Csr object context-manager."""
    try:
        csr_api = get_csr(table_name, cmc_name)
        yield csr_api
    finally:
        ...


def get_csr(table_name, cmc_instance: str = 'Commence.DB') -> Csr:
    """Create cached connection to Commence and return a Csr to operate on it."""
    cmc = Cmc(cmc_instance)
    csr_cmc = cmc.get_cursor(table_name)
    csr_api = Csr(csr_cmc, db_name=cmc.name)
    return csr_api


class Csr:
    def __init__(self, cursor: CsrCmc, db_name):
        self._cursor_cmc = cursor
        self.db_name = db_name

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


    def filter_by_field(
            self,
            field_name: str,
            condition: str,
            value: str = '',
            *,
            get=False,
            fslot: int = 1,
            empty: EmptyKind = 'raise',
    ) -> None | list[dict[str, str]]:
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        if not self._cursor_cmc.set_filter(filter_str):
            if empty == 'raise':
                raise types_api.CmcError(f'Error setting filter: {filter_str}')
            if empty == 'ignore':
                return
        if get:
            return self.records()

    def filter_by_connection(
            self,
            item_name: str,
            connection: types_api.Connection,
            *,
            get=False,
            fslot=1
    ) -> None | list[dict[str, str]]:
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        self._cursor_cmc.set_filter(filter_str)
        if get:
            return self.records()

    def filter_by_cmcfil(self, cmc_filter: types_api.CmcFilter, slot=1, *, get=False) -> None | \
                                                                                         list[
                                                                                             dict[
                                                                                                 str, str]]:
        self.filter_by_str(cmc_filter.filter_str(slot))
        if get:
            return self.records()

    def filter_by_array(self, fil_array: types_api.FilterArray, get=False) -> None | list[
        dict[str, str]]:
        for slot, fil in fil_array.filters.items():
            self.filter_by_cmcfil(fil, slot)
        if get:
            return self.records()

    def filter_by_str(self, filter_str: str):
        """ commence syntax filter string"""
        self._cursor_cmc.set_filter(filter_str)

    def clear_filter(self, slot=1):
        self.filter_by_str(f'[ViewFilter({slot},Clear)]')

    def filter_by_pk(self, pk: str, *, fslot=1, empty: EmptyKind = 'raise'):
        if not pk:
            raise ValueError('pk must be a non-empty string')
        self.filter_by_field(self.pk_label, 'Equal To', value=pk, fslot=fslot, empty=empty)
        if self.row_count == 0:
            if empty == 'raise':
                raise types_api.CmcError(f'No record found for {self.pk_label} {pk}')
        if self.row_count > 1:
            raise types_api.CmcError(f'Expected 1 record, got {self.row_count}')

    @contextlib.contextmanager
    def temporary_filter_pk(self, pk: str, *, slot=4, empty: EmptyKind = 'raise'):
        try:
            yield self.filter_by_pk(pk, fslot=slot, empty=empty)
        finally:
            self.clear_filter(slot)

    @contextlib.contextmanager
    def temporary_filter_fields(
            self,
            field_name: str,
            condition: str,
            value: str,
            *,
            slot=4,
            empty: EmptyKind = 'raise'
    ):
        try:
            yield self.filter_by_field(field_name, condition, value, fslot=slot, empty=empty)
        finally:
            self.clear_filter(slot)

    def get_named_addset(self, pk_val):
        row_set = self.get_add_rowset()
        row_set.modify_row(0, 0, pk_val)
        return row_set

    def get_add_rowset(self, count=1):
        return self._cursor_cmc.get_add_row_set(count=count)

    def get_edit_rowset(self, count=1):
        return self._cursor_cmc.get_edit_row_set(count=count)

    def get_delete_rowset(self, count=1):
        return self._cursor_cmc.get_delete_row_set(count=count)

    def get_query_rowset(self, count=1):
        return self._cursor_cmc.get_query_row_set(count=count)




# def records(self, count: int or None = None) -> list[dict[str, str]]:
#        row_set = self._cursor_cmc.get_query_row_set(count)
#        records = row_set.get_row_dicts()
#        return records
#
#    def one_record(self, pk_val: str) -> dict[str, str]:
#        with self.temporary_filter_pk(pk_val):
#            return self.records()[0]
#
#    def records_by_field(
#            self, field_name: str,
#            value: str,
#            max_rtn=None,
#            empty: _t.Literal['ignore', 'raise'] = 'raise'
#    ) -> list[dict[str, str]]:
#        """
#        Get records from the cursor by field name and value.
#
#        Args:
#            field_name: Name of the field to query.
#            value: Value to filter by.
#            max_rtn: Maximum number of records to return. If more than this, raise CmcError.
#            empty: Action to take if no records are found. Options are 'ignore', 'raise'.
#
#        Returns:
#            A list of dictionaries of field names and values for the record.
#
#        Raises:
#            CmcError: If the record is not found or if more than max_rtn records are found.
#
#        """
#        self.filter_by_field(field_name, 'Equal To', value, empty=empty)
#        records = self.records()
#        if not records and empty == 'raise':
#            raise types_api.CmcError(f'No record found for {field_name} {value}')
#        if max_rtn and len(records) > max_rtn:
#            raise types_api.CmcError(f'Expected max {max_rtn} records, got {len(records)}')
#        return records
#
#    def edit_record(
#            self,
#            pk_val: str,
#            package: dict,
#    ) -> bool:
#        """
#        Modify a record in the cursor and commit.
#
#        Args:
#            pk_val (str): The value for the primary key field.
#            package (dict): A dictionary of field names and values to modify.
#
#        Returns:
#            bool: True on success
#
#        """
#        with self.temporary_filter_pk(pk_val):
#            row_set = self._cursor_cmc.get_edit_row_set()
#            row_set.modify_row_dict(0, package)
#            return row_set.commit()
#
#    def delete_record(self, pk_val: str, empty: EmptyKind = 'raise'):
#        """
#        Delete a record from the cursor and commit.
#
#        Args:
#            pk_val (str): The value for the primary key field.
#            empty (str): Action to take if the record is not found. Options are 'ignore', 'raise'.
#
#        Returns:
#            bool: True on success
#
#        """
#        with self.temporary_filter_pk(pk_val, empty=empty):  # noqa: PyArgumentList
#            if self.row_count == 0 and empty == 'ignore':
#                return
#            row_set = self._cursor_cmc.get_delete_row_set()
#            row_set.delete_row(0)
#            res = row_set.commit()
#            return res
#
#    def add_record(
#            self,
#            pk_val: str,
#            package: dict,
#            existing: _t.Literal['replace', 'update', 'raise'] = 'raise'
#    ) -> bool:
#        """
#        Add and commit a record to the cursor.
#
#        Args:
#            pk_val: The value for the primary key field.
#            package: A dictionary of field names and values to add to the record.
#            existing: Action to take if the record already exists. Options are 'replace', 'update', 'raise'.
#
#        Returns:
#            bool: True on success
#
#        """
#        with self.temporary_filter_pk(pk_val, empty='ignore'):  # noqa: PyArgumentList
#            if self.row_count:
#                if existing == 'raise':
#                    raise types_api.CmcError('Record already exists')
#                elif existing == 'update':
#                    row_set = self._cursor_cmc.get_edit_row_set()
#                elif existing == 'replace':
#                    self.delete_record(pk_val, empty='ignore')
#                    row_set = self.get_named_addset(pk_val)
#            else:
#                row_set = self.get_named_addset(pk_val)
#
#            row_set.modify_row_dict(0, package)
#            res = row_set.commit()
#            return res
#
#        # try:
#        # except com_error as e:
#        #     # todo this is horrible. the error is related to threading but we are not using threading?
#        #     # maybe pywin32 uses threading when handling the underlying db error?
#        #     if e.hresult == -2147483617:
#        #         raise CmcError('Record already exists')
#        #     raise