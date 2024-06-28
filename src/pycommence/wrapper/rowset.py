from __future__ import annotations

import typing
from abc import ABC
from typing import TypeAlias

from . import enums_cmc
from .enums_cmc import OptionFlag, FLAGS_UNUSED

if typing.TYPE_CHECKING:
    from .cmc_csr import CursorWrapper
from ._icommence import (
    ICommenceAddRowSet, ICommenceDeleteRowSet, ICommenceEditRowSet,
    ICommenceQueryRowSet,
)

RowSetType: TypeAlias = ICommenceEditRowSet or ICommenceQueryRowSet or ICommenceAddRowSet or ICommenceDeleteRowSet


class RowSetBase(ABC):
    def __init__(self, cmc_rs: RowSetType):
        """
        Args:
            cmc_rs: A Commence Row Set object.

        """
        self._rs = cmc_rs

    @property
    def headers(self) -> list:
        """Returns a list of all column labels."""
        return [self.get_column_label(i) for i in range(self.column_count)]

    @property
    def column_count(self) -> int:
        """Returns the number of columns in the row set."""
        return self._rs.ColumnCount

    @property
    def row_count(self) -> int:
        """Returns the number of rows in the row set."""
        return self._rs.RowCount

    def get_value(
            self,
            row_index: int,
            column_index: int,
            cannonical: bool = True,
    ) -> str:
        """Retrieves the value at the specified row and column.

        Args:
            row_index: Index of the row.
            column_index: Index of the column.
            cannonical: True to return the value in canonical form.

        Returns:
            Value at the specified row and column.

        """
        flags = OptionFlag.CANONICAL.value if cannonical else FLAGS_UNUSED
        return self._rs.GetRowValue(row_index, column_index, flags)

    def get_column_label(self, index: int, by_field_name: bool = False) -> str:
        """Retrieves the label of the specified column.

        Args:
            index: Index of the column.
            by_field_name: True to return field label (ignore view labels).

        Returns:
            Label of the specified column.

        """
        flags = OptionFlag.FIELD_NAME.value if by_field_name else FLAGS_UNUSED
        return self._rs.GetColumnLabel(index, flags)

    def get_column_index(self, label: str, by_field_name:bool = False) -> int:
        """
        Searches and retrieves the index of the specified column label.

        Args:
            label: Label of the column.
            by_field_name: True to search by field name (ignore view labels).

        Returns:
            Index of the specified column label.

        """
        flags = OptionFlag.FIELD_NAME.value if by_field_name else FLAGS_UNUSED
        return self._rs.GetColumnIndex(label, flags)

    def get_row(
            self,
            row_index: int,
            delim: str = ';',
            cannonical: bool = True,
    ) -> str:
        """
        Retrieves the values of the specified row.

        Args:
            row_index: Index of the row.
            cannonical: True to return the value in canonical form.
            delim: Delimiter to use between values.

        Returns:
            Values of the specified row.

        """
        flags = OptionFlag.CANONICAL.value if cannonical else FLAGS_UNUSED
        return self._rs.GetRow(row_index, delim, flags)

    def get_row_id(self, row_index: int) -> str:
        """
        Retrieves the ID of the specified row.

        Args:
            row_index: Index of the row.

        Returns:
            ID of the specified row.

        """
        flags: int = enums_cmc.FLAGS_UNUSED
        return self._rs.GetRowID(row_index, flags)

    def get_row_dicts(self, num: int or None = None) -> list[dict[str, str]]:
        """Returns a dictionary of the first num rows."""
        if num is None:
            num = self.row_count
        labels = self.headers
        delim = '%^&*'
        rows = [self.get_row(i, delim=delim) for i in range(num)]
        return [dict(zip(labels, row.split(delim))) for row in rows]

    def get_shared(self, row_index: int) -> bool:
        """
        Determines whether the row at the specified index is shared.

        Args:
            row_index: Index of the row.

        Returns:
            True if the row is shared, False otherwise.

        """
        return self._rs.GetShared(row_index)


class RowSetQuery(RowSetBase):
    def __init__(self, cmc_rs: ICommenceQueryRowSet):
        super().__init__(cmc_rs)

    def get_field_to_file(
            self, row_index: int, column_index: int, file_path: str, cannonical: bool = True
    ) -> bool:
        """
        Saves the field value at the given (row, column) to a file.

        Args:
            row_index (int): The index of the row.
            column_index (int): The index of the column.
            file_path (str): The path where the field value will be saved to.
            cannonical (bool): True to save the value in canonical form.

        Returns:
            bool: True on success, False on failure.

        """
        flags = OptionFlag.CANONICAL.value if cannonical else FLAGS_UNUSED
        return self._rs.GetFieldToFile(row_index, column_index, file_path, flags)


class RowSetModifies(RowSetBase):
    """ adds functionality to modify rows """""

    def modify_row(self, row_index: int, column_index: int, value: str) -> bool:
        """
        Modifies a field value in the rowset.

        Args:
            row_index (int): The index of the row to modify.
            column_index (int): The index of the column in the row to modify.
            value (str): The new value for the field.

        Returns:
            bool: True on success, False on failure.

        """
        return self._rs.ModifyRow(row_index, column_index, value)

    def modify_row_dict(self, row_index: int, row_dict: dict) -> bool:
        """
        Modifies a row in the rowset.

        Args:
            row_index (int): The index of the row to modify.
            row_dict (dict): A dictionary of column names and values to modify.

        Returns:
            bool: True on success, False on failure.

        """
        for key, value in row_dict.items():
            if isinstance(value, bool):
                value = 'TRUE' if value else 'FALSE'
            col_idx = self.get_column_index(key)
            if col_idx == -1:
                raise ValueError(f'Invalid column name: {key}')
            self.modify_row(row_index, col_idx, value)
        return True

    def commit(self) -> bool:
        """
        Commit to disk.
        After Commit(), the RowSet is no Longer valid and should be discarded.

        Returns:
            bool: True on success, False on failure.

        """
        res = self._rs.Commit(enums_cmc.FLAGS_UNUSED)
        if res != 0:
            raise ValueError('Commit failed')
        return True

    def commit_get_cursor(self) -> CursorWrapper:
        """
        Makes row modifications permanent (commit to disk) and returns a cursor.

        Returns:
            CommenceCursor: Cursor object with the committed data.

        """
        return self._rs.CommitGetCursor(enums_cmc.FLAGS_UNUSED)


class RowSetAdd(RowSetModifies):
    """
    Represents a set of new items to add to the database.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.
        RowSetModifies: Base class for Write-Enabled RowSet objects.

    """

    def __init__(self, cmc_rs: ICommenceAddRowSet) -> None:
        """
        Initializes a RowSetAdd instance.
        Args:
            cmc_rs: A Commence Row Set object.
        """
        super().__init__(cmc_rs)


class RowSetDelete(RowSetModifies):
    """
    Represents a set of items to delete from the database.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.

    """

    def __init__(self, cmc_rs: ICommenceDeleteRowSet) -> None:
        """
        Initializes a RowSetDelete instance.

        Args:
            cmc_rs: A Commence Row Set object.

        """
        super().__init__(cmc_rs)

    def get_row_id(self, row_index: int) -> str:
        raise NotImplementedError(f"Can not get a row id for {self.__class__.__name__}.")

    def delete_row(self, row_index: int) -> bool:
        """
        Marks a row for deletion.
        Deletion is not permanent until Commit() is called.

        Args:
            row_index (int): The index of the row to mark for deletion.

        Returns:
            bool: True on success, False on failure.

        """
        return self._rs.DeleteRow(row_index, enums_cmc.FLAGS_UNUSED)

    def commit_get_cursor(self):
        raise NotImplementedError("Can not get a cursor for deleted rows.")

    def modify_row(self, row_index: int, column_index: int, value: str) -> bool:
        raise NotImplementedError("Can not modify a row for deletion.")


class RowSetEdit(RowSetModifies):
    def __init__(self, edit_rowset: ICommenceEditRowSet) -> None:
        """ cmc_rs: A Commence EditRowSet COM object. """
        super().__init__(edit_rowset)
