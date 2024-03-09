from typing import Optional

from loguru import logger

from . import cmc_enums as cenum, cmc_rowset as rs
from ._icommence import ICommenceCursor


class CsrCmc:
    """ Thin wrapper on the Commence Cursor object using pywin32.
     Create with CmcDb.GetCursor().
    """

    def __init__(self, cmc_cursor: ICommenceCursor):
        """ Internal use only. Use CmcDb.GetCursor() to create a cursor."""
        self._csr_cmc = cmc_cursor

    def __repr__(self):
        return f'CmcCursor: "{self.category}"'

    def __str__(self):
        return f'CmcCursor: "{self.category}"'

    @property
    def category(self):
        return self._csr_cmc.Category

    @property
    def column_count(self):
        return self._csr_cmc.ColumnCount

    @property
    def row_count(self):
        return self._csr_cmc.RowCount

    @property
    def shared(self):
        return self._csr_cmc.Shared

    def set_filter(self, filter_text: str):
        """
        Defines a filter clause for the cursor.

        Parameters:
            filter_text (str): Text defining the new filter clause.
            Syntax is identical to the one used by the DDE ViewFilter request.

        Raises:
            CmcError on fail
            ent.NotFoundError if filter returns no rows


        If the cursor is opened in CURSOR_VIEW mode, the set_filter only affects the cursor's secondary filter.
        That is, when building the rowset, the view's filter is first evaluated.
        Items that match are then passed through the cursor's secondary filter.
        The rowset only contains items that satisfy both filters.
        """
        res = self._csr_cmc.SetFilter(filter_text, cenum.FLAGS_UNUSED)
        if not res:
            raise ValueError(f'Could not set Commence filter {filter_text}')

    def set_filter_logic(self, logic_text: str):
        """
        Defines the filter logic for the cursor.

        Parameters:
        logic_text (str): Text defining the new filter logic.
        # todo filter logic builder
        Syntax is identical to the one used by the DDE ViewConjunction request.


        Comments:
        Unless otherwise specified, the default logic is AND, AND, AND.
        """
        logger.info(f'Setting filter logic to {logic_text}')
        res = self._csr_cmc.SetLogic(logic_text, cenum.FLAGS_UNUSED)
        if not res:
            logger.error(f'Unable to set filter logic to {logic_text}')
            raise ValueError('Unable to set filter logic')

    def set_sort(self, sort_text: str):
        """
        Defines the sort criteria for the cursor.

        Parameters:
        sort_text (str): Text defining the new sort criteria.
        Syntax is identical to the one used by the DDE ViewSort request.


        Comments:
        If the cursor is opened in CMC_CURSOR_VIEW mode, the sort defaults to the view's sort.
        All other cursor modes default to ascending sort by the Name field.
        """
        logger.info(f'Setting sort to {sort_text}')
        res = self._csr_cmc.SetSort(sort_text, cenum.FLAGS_UNUSED)
        if not res:
            logger.error(f'Unable to set sort to {sort_text}')
            raise ValueError("Unable to sort")

    def set_column(
            self, column_index: int, field_name: str,
            flags: Optional[cenum.OptionFlag] = cenum.OptionFlag.NONE
    ) -> bool:
        """
        Defines the column set for the cursor.

        Parameters:
        column_index (int): The (0-based) index of the column to set.
        field_name (str): Name of the field to use in this column.
        flags (int): Option flags (Logical OR of option flags like CMC_FLAG_ALL to create column set of all fields).

        Returns:
        bool: True on success, False on error.

        Comments:
        When defining a column set, the columns must be defined in sequential order (0, 1, 2, etc.).
        This is to prevent problems with undefined columns (e.g. 0, 1, 3, ...).
        Duplicate columns are not supported. Each column must map to a different field.
        Not all Commence field types can be included in the cursor definition.
        The set of supported field types exactly matches those fields that can be displayed in a Commence report
        (minus combined fields and indirect fields).
        """
        logger.info(f'Setting column {column_index} to {field_name}')
        res = self._csr_cmc.SetColumn(column_index, field_name, flags.value)
        if not res:
            raise ValueError("Unable to set column")
        return res

    def seek_row(self, start: int, rows: int) -> int:
        """
        Seek to a particular row in the cursor.

        Args:
            start (int): Position to move from. Can be one of the following:
                - 0 (BOOKMARK_BEGINNING) - from first row
                - 1 (BOOKMARK_CURRENT) - from current row
                - 2 (BOOKMARK_END) - from last row
            rows (int): Number of rows to move the current row pointer.

        Returns:
            int: Number of rows moved.

        Raises:
            CmcError on fail

        Comments:
        For any cursor, there is a 'current row pointer'. When the cursor is created, this defaults to the first row.
        SeekRow will reposition the current row pointer.
        GetQueryRowSet, GetEditRowSet, and GetDeleteRowSet will also advance the current row pointer.
        """
        res = self._csr_cmc.SeekRow(start, rows)
        if res == -1:
            raise ValueError(f"Unable to seek {rows} rows")
        return res

    def seek_row_fractional(self, numerator: int, denominator: int) -> int:
        """
        Seek to a fractional position in the cursor.

        Parameters:
        numerator (int): Numerator for fractional position in the cursor.
        denominator (int): Denominator for the fractional position in the cursor.

        Returns:
        int: Actual number of rows moved, -1 on error.
        """
        res = self._csr_cmc.SeekRowApprox(numerator, denominator)
        if res == -1:
            raise ValueError(
                f"Unable to seek {numerator}/{denominator} rows of {self.row_count} rows"
            )
        return res

    def get_query_row_set(self, count: int or None = None) -> rs.RowSetQuery:
        """
        Create a rowset object with the results of a query.

        Parameters:
        count (int): Maximum number of rows to retrieve.

        Returns:
        RowSetQuery: Pointer to rowset object on success, None on error.

        Comments:
        The rowset inherits the column set from the cursor.
        The cursor's 'current row pointer' determines the first row to be included in the rowset.
        The returned rowset can have fewer than count rows (e.g. if the current row pointer is near the end).
        Use CommenceXRowSet.row_count to determine the actual row count.
        GetQueryRowSet will advance the 'current row pointer' by the number of rows in the rowset.
        """
        if count is None:
            count = self.row_count
        result = self._csr_cmc.GetQueryRowSet(count, cenum.FLAGS_UNUSED)
        if result.rowcount == 0:
            raise ValueError()
        return rs.RowSetQuery(result)

    def get_query_row_set_by_id(self, row_id: str, *, flags=0):
        """
        Returns: Pointer to rowset object on success, NULL on error.
        Parameters:
            row_id:str Unique ID string obtained from GetRowID().
            flags: unused, must be 0.
        The rowset inherits column set from the cursor.
        The cursor's 'current row pointer' is not advanced.

        """
        res = rs.RowSetQuery(self._csr_cmc.GetQueryRowSetByID(row_id, cenum.FLAGS_UNUSED))
        if res.row_count == 0:
            raise ValueError()
        return res

    def get_add_row_set(
            self, count: int or None = None,
            flags: Optional[cenum.OptionFlag] = cenum.OptionFlag.NONE
    ) -> rs.RowSetAdd:
        """
        Creates a rowset of new items to add to the database.

        Parameters:
        count (int): The number of rows to create.
        flags (int): Option flags. Use CMC_FLAG_SHARED to default all rows to shared. Defaults to 0.

        Returns:
        RowSetAdd: A rowset object for adding new items.

        Comments:
        The rowset inherits the column set from the cursor.
        When first created, each row is initialized to field default values.
        """
        if count is None:
            count = self.row_count
        res = rs.RowSetAdd(self._csr_cmc.GetAddRowSet(count, flags.value))
        if res.row_count == 0:
            raise ValueError()
        return res

    def get_edit_row_set(self, count: int or None = None) -> rs.RowSetEdit:
        """
        Creates a rowset of existing items for editing.

        Parameters:
        count (int): The number of rows to retrieve.
        flags (int, optional): Unused at present, must be 0. Defaults to 0.

        Returns:
        RowSetEdit: A rowset object for editing existing items, or None on error.

        Comments:
        The rowset inherits the column set from the cursor.
        """
        if count is None:
            count = self.row_count
        return rs.RowSetEdit(self._csr_cmc.GetEditRowSet(count, cenum.FLAGS_UNUSED))

    def get_edit_row_set_by_id(self, row_id: str) -> rs.RowSetEdit:
        """
        Creates a rowset for editing a particular row.

        Parameters:
        row_id (str): Unique ID string obtained from GetRowID().
        flags (int, optional): Unused at present, must be 0. Defaults to 0.

        Returns:
        RowSetEdit: A rowset object for editing a particular row, or None on error.

        Comments:
        The rowset inherits the column set from the cursor.
        The cursor's 'current row pointer' is not advanced.
        """
        res = rs.RowSetEdit(
            self._csr_cmc.GetEditRowSetByID(
                row_id,
                cenum.FLAGS_UNUSED
            )
        )
        if res.row_count == 0:
            raise ValueError()
        return res

    def get_delete_row_set(self, count: int or None = None) -> rs.RowSetDelete:
        """
        Creates a rowset of existing items for deletion.

        Parameters:
        count (int): The number of rows to retrieve.
        flags (int, optional): Unused at present, must be 0. Defaults to 0.

        Returns:
        RowSetDelete: A rowset object for deleting existing items, or None on error.

        Comments:
        The rowset inherits the column set from the cursor.
        """
        if count is None:
            count = self.row_count
        if count > 1:
            check = input(f'Are you sure you want to delete {self.row_count} rows? (y/n)')
            if check.lower() != 'y':
                raise ValueError('Aborted deletion.')
        rs = self._csr_cmc.GetDeleteRowSet(count, 0)
        return rs.RowSetDelete(rs)

    def get_delete_row_set_by_id(
            self, row_id: str,
            flags: cenum.OptionFlag = cenum.OptionFlag.NONE
    ) -> rs.RowSetDelete:
        """
        Creates a rowset for deleting a particular row.

        Parameters:
        row_id (str): Unique ID string obtained from GetRowID().
        flags (int, optional): Unused at present, must be 0. Defaults to 0.

        Returns:
        RowSetDelete: A rowset object for deleting a particular row, or None on error.

        Comments:
        The rowset inherits the column set from the cursor.
        The cursor's 'current row pointer' is not advanced.
        """
        return rs.RowSetDelete(self._csr_cmc.GetDeleteRowSetByID(row_id, flags.value))

    def set_active_item(self, category: str, row_id: str):
        """
        Set active item used for view cursors using a view linking filter_str.

        Parameters:
        category (str): Category name of the active item used with view linking filter_str.
        row_id (str): Unique ID string obtained from GetRowID()
        indicating the active item used with view linking filter_str.

        Returns:
        bool: True on success, else False on error.
        """
        return self._csr_cmc.SetActiveItem(category, row_id, cenum.FLAGS_UNUSED)

    def set_active_date(self, active_date: str):
        """
        Set active active_date used for view cursors using a view linking filter_str.

        Parameters:
        active_date (str): Date value used with view linking filter_str; supports AI active_date values such as 'today'.

        Returns:
        bool: True on success, else False on error.
        """
        return self._csr_cmc.SetActiveDate(active_date, cenum.FLAGS_UNUSED)

    def set_active_date_range(self, start: str, end: str):
        """
        Set active active_date range used for view cursors using a view linking filter_str.

        Parameters:
        start (str): Date value of start active_date used with view linking filter_str;
        supports AI active_date values such as 'today'.
        end (str): Date value of end active_date used with view linking filter_str;
        supports AI active_date values such as 'next monday'.
        flags (int, optional): Unused at present, must be 0. Defaults to 0.

        Returns:
        bool: True on success, else False on error.
        """
        return self._csr_cmc.SetActiveDateRange(start, end, cenum.FLAGS_UNUSED)

    def set_related_column(
            self, col: int, con_name: str, connected_cat: str, col_name: str,
            flags: Optional[cenum.OptionFlag] = cenum.OptionFlag.NONE
    ):
        """
        Adds a related (indirect/connected field) column to the cursor.

        Parameters:
        col (int): The (0-based) index of the column to set.
        con_name (str): Name of the connection to use in this column.
        connected_cat (str): Name of the connected Category to use in this column.
        name (str): Name of the field in the connected category to use in this column.
        flags (int): Option flags (Logical OR of option flags like CMC_FLAG_ALL to create column set of all fields).

        Returns:
        bool: True on success, False on error.

        Example:
        set_related_column(0, "Relates To", "History", "Date", 0)
        This call will add the Date field to the cursor via the 'Relates to History' connection.
        """
        return self._csr_cmc.SetRelatedColumn(col, con_name, connected_cat, col_name, flags.value)
