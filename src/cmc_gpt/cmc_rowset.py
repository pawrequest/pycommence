class RowSetBase:
    """
    Base class representing a Commence Row Set.

    Attributes:
        _rs: Internal representation of a Commence Row Set object.
    """

    def __init__(self, cmc_rs) -> None:
        """
        Initializes a RowSetBase instance.

        Args:
            cmc_rs: A Commence Row Set object.
        """
        self._rs = cmc_rs

    @property
    def all_column_labels(self) -> list:
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

    def get_row_value(self, row_index: int, column_index: int, flags: int = 0) -> str:
        """
        Retrieves the value at the specified row and column.

        Args:
            row_index: Index of the row.
            column_index: Index of the column.
            flags: Logical OR of following option flags:
                    CMC_FLAG_CANONICAL - return field value in canonical form
        Returns:
            Value at the specified row and column.

        """
        return self._rs.GetRowValue(row_index, column_index, flags)

    def get_column_label(self, index: int, flags=0) -> str:
        """
        Retrieves the label of the specified column.

        Args:
            index: Index of the column.
            flags: Logical OR of following option flags:
                CMC_FLAG_FIELD_NAME - return field label (ignore view labels)

        Returns:
            Label of the specified column.
        """
        return self._rs.GetColumnLabel(index, flags)

    def get_column_index(self, label: str, flags: int = 0) -> int:
        """
        Searches and retrieves the index of the specified column label.

        Args:
            label: Label of the column.
            flags: Logical OR of following option flags:
                    CMC_FLAG_FIELD_NAME - return field label (ignore view labels)


        Returns:
            Index of the specified column label.
        """
        return self._rs.GetColumnIndex(label, flags)

    def get_row(self, row_index: int, delim: str = ';', flags: int = 0) -> str:
        """
        Retrieves the values of the specified row.

        Args:
            row_index: Index of the row.
            flags: Logical OR of following option flags:
                    CMC_FLAG_CANONICAL - return field value in canonical form

        Returns:
            Values of the specified row.
        """
        return self._rs.GetRow(row_index, delim, flags)

    def get_rows_dict(self, num):
        """Returns a dictionary of the first num rows."""
        labels = self.all_column_labels
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


class RowSetAdd(RowSetBase):
    """
    Represents a set of new items to add to the database.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.
    """

    def commit(self) -> bool:
        """
        Makes row modifications permanent (commit to disk).

        Args:
            flags: Unused at present, must be 0.
        Returns:
            bool: True on success, False on failure.
        After Commit(), the ICommenceAddRowSet is no Longer valid and should be discarded.
        """
        return self._rs.Commit(0)

    def commit_get_cursor(self) -> 'CommenceCursor':
        """
        Makes row modifications permanent (commit to disk) and returns a cursor.

        Returns:
            CommenceCursor: Cursor object with the committed data.
        """
        return self._rs.CommitGetCursor(0)


class RowSetDelete(RowSetBase):
    """
    Represents a set of items to delete from the database.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.
    """

    def delete_row(self, row_index: int) -> bool:
        """
        Marks a row for deletion.

        Args:
            row_index (int): The index of the row to mark for deletion.
            flags: Unused at present, must be 0.

        Returns:
            bool: True on success, False on failure.
        Deletion is not permanent until Commit() is called.
        """
        return self._rs.DeleteRow(row_index, 0)

    def commit(self) -> bool:
        """
        Makes row deletions permanent (commit to disk).

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.Commit(0)


class RowSetEdit(RowSetBase):
    """
    Represents a set of items to edit in the database.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.
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
        return self._rs.ModifyRow(row_index, column_index, value, 0)

    def commit(self) -> bool:
        """
        Makes row modifications permanent (commit to disk).

        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.Commit(0)

    def commit_get_cursor(self) -> 'CommenceCursor':
        """
        Makes row modifications permanent (commit to disk) and returns a cursor.

        Returns:
            CommenceCursor: Cursor object with the committed data.
        """
        return self._rs.CommitGetCursor(0)


class RowSetQuery(RowSetBase):
    """
    Represents a result set from a query.

    Inherits from:
        RowSetBase: Base class for Commence Row Set objects.
    """

    def get_field_to_file(
            self, row_index: int, column_index: int, file_path: str, flags: int = 0
    ) -> bool:
        """
        Saves the field value at the given (row, column) to a file.

        Args:
            row_index (int): The index of the row.
            column_index (int): The index of the column.
            file_path (str): The path where the field value will be saved to.
            flags: Logical OR of following option flags:
                    CMC_FLAG_CANONICAL - return field value in canonical form



        Returns:
            bool: True on success, False on failure.
        """
        return self._rs.GetFieldToFile(row_index, column_index, file_path, flags)
