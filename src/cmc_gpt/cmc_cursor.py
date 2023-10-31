
class CommenceCursor:
    def __init__(self, commence_cursor):
        self.commence_cursor = commence_cursor

    @property
    def category(self):
        return self.commence_cursor.Category

    @property
    def column_count(self):
        return self.commence_cursor.ColumnCount

    @property
    def row_count(self):
        return self.commence_cursor.RowCount

    @property
    def shared(self):
        return self.commence_cursor.Shared

    def set_column(self, nColumn, pName, nFlags):
        return self.commence_cursor.SetColumn(nColumn, pName, nFlags)

    def set_filter(self, pFilter, nFlags):
        return self.commence_cursor.SetFilter(pFilter, nFlags)

    def set_logic(self, pLogic, nFlags):
        return self.commence_cursor.SetLogic(pLogic, nFlags)

    def set_sort(self, pLogic, nFlags):
        return self.commence_cursor.SetSort(pLogic, nFlags)

    def seek_row(self, bkOrigin, nRows):
        return self.commence_cursor.SeekRow(bkOrigin, nRows)

    def seek_row_approx(self, nNumerator, nDenom):
        return self.commence_cursor.SeekRowApprox(nNumerator, nDenom)

    def get_query_row_set(self, nCount, nFlags):
        return CommenceQueryRowSet(self.commence_cursor.GetQueryRowSet(nCount, nFlags))

    def get_query_row_set_by_id(self, pRowID, nFlags):
        return CommenceQueryRowSet(self.commence_cursor.GetQueryRowSetByID(pRowID, nFlags))

    def get_add_row_set(self, nCount, nFlags):
        return CommenceAddRowSet(self.commence_cursor.GetAddRowSet(nCount, nFlags))

    def get_edit_row_set(self, nCount, nFlags):
        return CommenceEditRowSet(self.commence_cursor.GetEditRowSet(nCount, nFlags))

    def get_edit_row_set_by_id(self, pRowID, nFlags):
        return CommenceEditRowSet(self.commence_cursor.GetEditRowSetByID(pRowID, nFlags))

    def get_delete_row_set(self, nCount, nFlags):
        return CommenceDeleteRowSet(self.commence_cursor.GetDeleteRowSet(nCount, nFlags))

    def get_delete_row_set_by_id(self, pRowID, nFlags):
        return CommenceDeleteRowSet(self.commence_cursor.GetDeleteRowSetByID(pRowID, nFlags))

    def set_active_item(self):
        return self.commence_cursor.SetActiveItem()

    def set_active_date(self):
        return self.commence_cursor.SetActiveDate()

    def set_active_date_range(self):
        return self.commence_cursor.SetActiveDateRange()

    def set_related_column(self):
        return self.commence_cursor.SetRelatedColumn()