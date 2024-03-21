"""
API for Commence Cursor (Csr) objects.
provides access to the Commence Cursor object and methods to interact with it.
"""
from __future__ import annotations

import typing as _t
import contextlib
from typing import TYPE_CHECKING

from loguru import logger
from win32com.universal import com_error

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
    try:
        cmc = Cmc(cmc_name)
        csr_cmc = cmc.get_cursor(table_name)
        csr_api = Csr(csr_cmc)
        return csr_api
    except Exception as e:
        logger.error(f'Error in get_csr: {e}')


class Csr:
    def __init__(self, cursor: CsrCmc):
        self._cursor_cmc = cursor

    def edit_record(self, name: str, package: dict) -> None:
        """Modify a record in the cursor and commit.

        Args:
            name (str): Name of the record to modify.
            package (dict): A dictionary of field names and values to modify.
            """
        self.filter_by_name(name)
        row_set = self._cursor_cmc.get_edit_row_set()
        for key, value in package.items():
            try:
                col_idx = row_set.get_column_index(key)
                row_set.modify_row(0, col_idx, str(value))
            except Exception:
                raise CmcError(f'Could not modify {key} to {value}')
        row_set.commit()

    # def get_record_by_name(self, record_name: str) -> dict[str, str]:
    #     """Get a record from the cursor by Column[0].
    #     Args:
    #         record_name (str): Name of the record to get.
    #     Returns:
    #         dict[str, str]: A dictionary of field names and values for the record.
    #     Raises:
    #         CmcError: If the record is not found or if more than one record is found.
    #         """
    #     self.filter_by_name(record_name)
    #     records = self.get_records()
    #     if not records:
    #         raise CmcError(f'No record found for {record_name}')
    #     if len(records) > 1:
    #         raise CmcError(f'Expected 1 record, got {len(records)}')
    #     return records[0]

    def records_by_field(self, field_name: str, value: str, max_rtn=None) -> list[dict[str, str]]:
        """Get a record from the cursor by Column[0].
        Args:
            field_name (str): Name of the field to query.
            value (str): Value to filter by.
            max_rtn (int): Maximum number of records to return. If more than this, raise CmcError.
        Returns:
            dict[str, str]: A dictionary of field names and values for the record.
        Raises:
            CmcError: If the record is not found or if more than max_rtn records are found.
            """
        self.filter_by_field(field_name, 'Equal To', value)
        records = self.get_records()
        if not records:
            raise CmcError(f'No record found for {field_name} {value}')
        if max_rtn and len(records) > max_rtn:
            raise CmcError(f'Expected max {max_rtn} records, got {len(records)}')
        return records

    def record_by_name(self, name: str) -> dict[str, str]:
        return self.records_by_field('Name', name, 1)[0]

    def get_records(self, count: int or None = None) -> list[dict[str, str]]:
        row_set = self._cursor_cmc.get_query_row_set(count)
        records = row_set.get_rows_dict()
        return records

    def delete_record(self, record_name):
        try:
            self.filter_by_name(record_name)
            row_set = self._cursor_cmc.get_delete_row_set()
            row_set.delete_row(0)
            res = row_set.commit()
            return res
        except Exception:
            ...

    def add_record(
            self,
            col_0: str,
            package: dict,
            exists: _t.Literal['replace', 'update', 'raise'] = 'raise'
    ) -> bool:
        """
        Add and commit a record to the cursor.

        Args:
            record_name (str): Name of the record to add at column0.
            package (dict): A dictionary of field names and values to add to the record.
            allow_dupe (bool): If False, raise CmcError if record already exists.

        Returns:
            bool: True on success, False on failure.
            """
        match exists:
            case 'raise':
                pass
            case 'replace':
                self.delete_record(col_0)
            case 'update':
                self.edit_record(col_0, package)
        try:
            row_set = self._cursor_cmc.get_add_row_set(1)
            row_set.modify_row(0, 0, col_0)
            row_set.modify_row_dict(0, package)
            res = row_set.commit()
            return res

        except com_error as e:
            # todo this is horrible. the error is related to threading but we are not using threading?
            # maybe pywin32 uses threading when handling the underlying db error?
            if e.hresult == -2147483617:
                raise CmcError('Record already exists')
            raise

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
            return self.get_records()

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
            return self.get_records()

    def filter_by_cmcfil(self, cmc_filter: CmcFilter, slot=1, *, get=False) -> None | list[
        dict[str, str]]:
        self.filter_by_str(cmc_filter.filter_str(slot))
        if get:
            return self.get_records()

    def filter_by_array(self, fil_array: FilterArray, get=False) -> None | list[dict[str, str]]:
        for slot, fil in fil_array.filters.items():
            self.filter_by_cmcfil(fil, slot)
        if get:
            return self.get_records()

    def filter_by_str(self, filter_str: str):
        self._cursor_cmc.set_filter(filter_str)

    def filter_by_name(self, name: str, *, fslot=1):
        self.filter_by_field('Name', 'Equal To', value=name, fslot=fslot)

    def filter_by_col0(self, col0: str, *, fslot=1):
        self.filter_by_field('Column[0]', 'Equal To', value=col0, fslot=fslot)

    # def set_filters(self, filters: list[CmcFilter], get_all=False):
    #     for i, fil in enumerate(filters, start=1):
    #         self.filter_by_cmcfil(fil, i)
    #     if get_all:
    #         return self.get_records()
