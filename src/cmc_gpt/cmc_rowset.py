from cmc_gpt.cmc_cursor import CommenceCursor


class BaseRowSet:
    """
    Base class representing a Commence Row Set.

    Attributes:
        _rs: Internal representation of a Commence Row Set object.
    """

    def __init__(self, cmc_rs) -> None:
        """
        Initializes a BaseRowSet instance.

        Args:
            cmc_rs: A Commence Row Set object.
        """
        self._rs = cmc_rs

    @property
    def column_count(self) -> int:
        """Returns the number of columns in the row set."""
        return self._rs.ColumnCount

    @property
    def row_count(self) -> int:
        """Returns the number of rows in the row set."""
        return self._rs.RowCount

    def get_row_value(self, row_index: int, column_index: int) -> str:
        """
        Retrieves the value at the specified row and column.

        Args:
            row_index: Index of the row.
            column_index: Index of the column.

        Returns:
            Value at the specified row and column.
        """
        return self._rs.GetRowValue(row_index, column_index)

    def get_column_label(self, index: int) -> str:
        """
        Retrieves the label of the specified column.

        Args:
            index: Index of the column.

        Returns:
            Label of the specified column.
        """
        return self._rs.GetColumnLabel(index)

    def get_column_index(self, label: str) -> int:
        """
        Searches and retrieves the index of the specified column label.

        Args:
            label: Label of the column.

        Returns:
            Index of the specified column label.
        """
        return self._rs.GetColumnIndex(label)

    def get_row(self, row_index: int) -> str:
        """
        Retrieves the values of the specified row.

        Args:
            row_index: Index of the row.

        Returns:
            Values of the specified row.
        """
        return self._rs.GetRow(row_index)

    def get_shared(self, row_index: int) -> bool:
        """
        Determines whether the row at the specified index is shared.

        Args:
            row_index: Index of the row.

        Returns:
            True if the row is shared, False otherwise.
        """
        return self._rs.GetShared(row_index)


class RowSetAdd(BaseRowSet):
    """
    Represents a set of new items to add to the database.

    Inherits from:
        BaseRowSet: Base class for Commence Row Set objects.
    """

    def commit(self, flags: int = 0) -> bool:
        """
        Makes row modifications permanent (commit to disk).

        Args:
            flags (int, optional): Flags for the commit operation. Defaults to 0.

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.Commit(flags)

    def commit_get_cursor(self) -> CommenceCursor:
        """
        Makes row modifications permanent (commit to disk) and returns a cursor.

        Returns:
            CommenceCursor: Cursor object with the committed data.
        """
        return CommenceCursor(self._rs.CommitGetCursor())


class RowSetDelete(BaseRowSet):
    """
    Represents a set of items to delete from the database.

    Inherits from:
        BaseRowSet: Base class for Commence Row Set objects.
    """

    def delete_row(self, row_index: int) -> bool:
        """
        Marks a row for deletion.

        Args:
            row_index (int): The index of the row to mark for deletion.

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.DeleteRow(row_index)

    def commit(self) -> bool:
        """
        Makes row deletions permanent (commit to disk).

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.Commit()


class RowSetEdit(BaseRowSet):
    """
    Represents a set of items to edit in the database.

    Inherits from:
        BaseRowSet: Base class for Commence Row Set objects.
    """

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

    def commit(self) -> bool:
        """
        Makes row modifications permanent (commit to disk).

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.Commit()

    def commit_get_cursor(self) -> 'CommenceCursor':
        """
        Makes row modifications permanent (commit to disk) and returns a cursor.

        Returns:
            CommenceCursor: Cursor object with the committed data.
        """
        return CommenceCursor(self._rs.CommitGetCursor())


class RowSetQuery(BaseRowSet):
    """
    Represents a result set from a query.

    Inherits from:
        BaseRowSet: Base class for Commence Row Set objects.
    """

    def get_field_to_file(self, row_index: int, column_index: int, file_path: str) -> bool:
        """
        Saves the field value at the given (row, column) to a file.

        Args:
            row_index (int): The index of the row.
            column_index (int): The index of the column.
            file_path (str): The path where the field value will be saved to.

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.GetFieldToFile(row_index, column_index, file_path)
