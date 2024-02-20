from __future__ import annotations

import re
from datetime import date, datetime, time
from decimal import Decimal
from typing import TYPE_CHECKING

from win32com.universal import com_error

from pycommence.entities import CmcError, Connection
from pycommence.filters import CmcFilter, FilterArray, CmcFilterPy

if TYPE_CHECKING:
    from pycommence.wrapper.cmc_cursor import CsrCmc


class Csr:
    def __init__(self, cursor: CsrCmc):
        self._cursor = cursor

    def edit_record(self, name: str, package: dict) -> None:
        """Modify a record in the cursor and commit.

        Args:
            name (str): Name of the record to modify.
            package (dict): A dictionary of field names and values to modify.
            """
        self.filter_by_name(name)
        row_set = self._cursor.get_edit_row_set()
        for key, value in package.items():
            try:
                col_idx = row_set.get_column_index(key)
                row_set.modify_row(0, col_idx, str(value))
            except Exception:
                raise CmcError(f'Could not modify {key} to {value}')
        row_set.commit()

    def get_record(self, record_name: str) -> dict[str, str]:
        """Get a record from the cursor by name (Column[0]).
        Args:
            record_name (str): Name of the record to get.
        Returns:
            dict[str, str]: A dictionary of field names and values for the record.
        Raises:
            CmcError: If the record is not found or if more than one record is found.
            """
        self.filter_by_name(record_name)
        records = self.get_all_records()
        if not records:
            raise CmcError(f'No record found for {record_name}')
        if len(records) > 1:
            raise CmcError(f'Expected 1 record, got {len(records)}')
        return records[0]

    def get_all_records(self) -> list[dict[str, str]]:
        row_set = self._cursor.get_query_row_set()
        records = row_set.get_rows_dict()
        return records

    def delete_record(self, record_name):
        try:
            self.filter_by_name(record_name)
            row_set = self._cursor.get_delete_row_set()
            row_set.delete_row(0)
            res = row_set.commit()
            return res
        except Exception:
            ...

    def add_record(self, record_name: str, package: dict) -> bool:
        """
        Add and commit a record to the cursor.

        Args:
            record_name (str): Name of the record to add at column0.
            package (dict): A dictionary of field names and values to add to the record.

        Returns:
            bool: True on success, False on failure.
            """
        try:
            row_set = self._cursor.get_add_row_set(1)
            row_set.modify_row(0, 0, record_name)
            row_set.modify_row_dict(0, package)
            res = row_set.commit()
            return res

        except com_error as e:
            # todo this is horrible. the error is due to threading but we are not using threading?
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
            fslot: int = 1
    ) -> None:
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        self._cursor.set_filter(filter_str)

    def filter_by_connection(
            self,
            item_name: str,
            connection: Connection,
            *,
            fslot=1
    ):
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        self._cursor.set_filter(filter_str)

    def filter_by_name(self, name: str, *, fslot=1):
        self.filter_by_field('Name', 'Equal To', value=name, fslot=fslot)

    def filter(self, cmc_filter: CmcFilter, slot=1):
        self.filter_by_str(cmc_filter.filter_str(slot))

    def filter_py(self, cmc_filter: CmcFilterPy, slot=1):
        self.filter_by_str(cmc_filter.filter_str(slot))

    def filter_by_str(self, filter_str: str):
        self._cursor.set_filter(filter_str)

    def set_filters(self, filters: list[CmcFilter], get_all=False):
        for i, fil in enumerate(filters, start=1):
            self.filter(fil, i)
        if get_all:
            return self.get_all_records()

    def filter_by_array(self, fil_array: FilterArray, get_all=False) -> None | list[dict[str, str]]:
        for slot, fil in fil_array.filters.items():
            self.filter(fil, slot)
        if get_all:
            return self.get_all_records()

    # @property
    # def get_schema(self):
    #     # NOPE this gets incimplete schema (missing types) if row does not have all ttrs
    #     rs = self._cursor.get_query_row_set(1)
    #     row = rs.get_rows_dict()[0]
    #     scm = {
    #         k: type(infer_and_parse(v))
    #         for k, v in row.items()
    #     }
    #     return scm


def infer_and_parse(value: str) -> date | time | Decimal | bool | str | None:
    value = value.strip()

    # date
    if re.match(r'\d{1,2}/\d{1,2}/\d{4}', value):
        return datetime.strptime(value, '%d/%m/%Y').date()

    # time
    if re.match(r'^\d{2}:\d{2}', value):
        return datetime.strptime(value, "%I:%M %p").time()

    # bool
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'

    # num
    if value.isnumeric():
        if '.' in value:
            try:
                value = Decimal(value)
            except Exception:
                value = float(value)
        value = int(value)

    return value or None
