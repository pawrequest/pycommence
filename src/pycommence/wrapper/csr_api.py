from __future__ import annotations

from typing import TYPE_CHECKING

from win32com.universal import com_error
from pycommence.entities import CmcError, Connection

if TYPE_CHECKING:
    from pycommence.wrapper.cmc_cursor import CmcCursor


class CsrApi:
    def __init__(self, cursor: CmcCursor):
        self.cursor = cursor

    def filter_by_field(self, field_name: str, condition: str, value: str = '', *, fslot: int = 1):
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        res = self.cursor.set_filter(filter_str)
        return res

    def filter_by_connection(self, item_name: str, connection: Connection, fslot=1):
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        res = self.cursor.set_filter(filter_str)
        if not res:
            raise ValueError(f'Could not set filter for ' f'{connection.name} = {item_name}')
        # todo return

    def filter_by_name(self, name: str, fslot=1):
        res = self.filter_by_field('Name', 'Equal To', value=name, fslot=fslot)
        return res

    def edit_record(self, name, package: dict):
        self.filter_by_name(name)
        row_set = self.cursor.get_edit_row_set()
        for key, value in package.items():
            try:
                col_idx = row_set.get_column_index(key)
                row_set.modify_row(0, col_idx, str(value))
            except Exception:
                raise CmcError(f'Could not modify {key} to {value}')
        row_set.commit()
        ...

    def get_record_one(self, record_name):
        res = self.filter_by_name(record_name)
        if not res:
            raise CmcError(f'Could not find {record_name}')
        row_set = self.cursor.get_query_row_set()
        if row_set.row_count != 1:
            raise CmcError(f'Expected 1 record, got {row_set.row_count}')
        record = row_set.get_rows_dict()[0]
        return record

    def get_records(self):
        row_set = self.cursor.get_query_row_set()
        records = row_set.get_rows_dict()
        return records

    def delete_record(self, record_name):
        try:
            self.filter_by_name(record_name)
            row_set = self.cursor.get_delete_row_set()
            row_set.delete_row(0)
            res = row_set.commit()
            return res
        except Exception:
            ...

    def add_record(self, record_name: str, package: dict) -> bool:
        """
        Adds a record to the cursor.

        Args:
            record_name (str): Name of the record to add at column0.
            package (dict): A dictionary of field names and values to add to the record.

        Returns:
            bool: True on success, False on failure.
            """
        try:
            row_set = self.cursor.get_add_row_set(1)
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
