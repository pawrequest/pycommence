from cmc_gpt.cmc_cursor import CommenceCursor


class CommenceAddRowSet:
    def __init__(self, commence_add_row_set):
        self.commence_add_row_set = commence_add_row_set

    @property
    def column_count(self):
        return self.commence_add_row_set.ColumnCount

    @property
    def row_count(self):
        return self.commence_add_row_set.RowCount

    def commit(self):
        return self.commence_add_row_set.Commit()

    def commit_get_cursor(self):
        return CommenceCursor(self.commence_add_row_set.CommitGetCursor())

    def get_column_index(self, label):
        return self.commence_add_row_set.GetColumnIndex(label)

    def get_column_label(self, index):
        return self.commence_add_row_set.GetColumnLabel(index)

    def get_row(self, row_index):
        return self.commence_add_row_set.GetRow(row_index)

    def get_row_value(self, row_index, column_index):
        return self.commence_add_row_set.GetRowValue(row_index, column_index)

    def modify_row(self, row_index, column_index, value):
        return self.commence_add_row_set.ModifyRow(row_index, column_index, value)

    def set_shared(self, row_index, shared):
        return self.commence_add_row_set.SetShared(row_index, shared)

    def get_shared(self, row_index):
        return self.commence_add_row_set.GetShared(row_index)


class CommenceDeleteRowSet:
    def __init__(self, commence_delete_row_set):
        self.commence_delete_row_set = commence_delete_row_set

    @property
    def column_count(self):
        return self.commence_delete_row_set.ColumnCount

    @property
    def row_count(self):
        return self.commence_delete_row_set.RowCount

    def get_row_value(self, row_index, column_index):
        return self.commence_delete_row_set.GetRowValue(row_index, column_index)

    def get_column_label(self, index):
        return self.commence_delete_row_set.GetColumnLabel(index)

    def get_column_index(self, label):
        return self.commence_delete_row_set.GetColumnIndex(label)

    def delete_row(self, row_index):
        return self.commence_delete_row_set.DeleteRow(row_index)

    def commit(self):
        return self.commence_delete_row_set.Commit()

    def get_row(self, row_index):
        return self.commence_delete_row_set.GetRow(row_index)

    def get_row_id(self, row_index):
        return self.commence_delete_row_set.GetRowID(row_index)

    def get_shared(self, row_index):
        return self.commence_delete_row_set.GetShared(row_index)


class CommenceEditRowSet:
    def __init__(self, commence_edit_row_set):
        self.commence_edit_row_set = commence_edit_row_set

    @property
    def column_count(self):
        return self.commence_edit_row_set.ColumnCount

    @property
    def row_count(self):
        return self.commence_edit_row_set.RowCount

    def get_row_value(self, row_index, column_index):
        return self.commence_edit_row_set.GetRowValue(row_index, column_index)

    def get_column_label(self, index):
        return self.commence_edit_row_set.GetColumnLabel(index)

    def get_column_index(self, label):
        return self.commence_edit_row_set.GetColumnIndex(label)

    def modify_row(self, row_index, column_index, value):
        return self.commence_edit_row_set.ModifyRow(row_index, column_index, value)

    def commit(self):
        return self.commence_edit_row_set.Commit()

    def commit_get_cursor(self):
        return CommenceCursor(self.commence_edit_row_set.CommitGetCursor())

    def get_row(self, row_index):
        return self.commence_edit_row_set.GetRow(row_index)

    def get_shared(self, row_index):
        return self.commence_edit_row_set.GetShared(row_index)

    def set_shared(self, row_index, shared):
        return self.commence_edit_row_set.SetShared(row_index, shared)

    def get_row_id(self, row_index):
        return self.commence_edit_row_set.GetRowID(row_index)


class CommenceQueryRowSet:
    def __init__(self, commence_query_row_set):
        self.commence_query_row_set = commence_query_row_set

    @property
    def column_count(self):
        return self.commence_query_row_set.ColumnCount

    @property
    def row_count(self):
        return self.commence_query_row_set.RowCount

    def get_row_value(self, row_index, column_index):
        return self.commence_query_row_set.GetRowValue(row_index, column_index)

    def get_column_label(self, index):
        return self.commence_query_row_set.GetColumnLabel(index)

    def get_column_index(self, label):
        return self.commence_query_row_set.GetColumnIndex(label)

    def get_row(self, row_index):
        return self.commence_query_row_set.GetRow(row_index)

    def get_row_id(self, row_index):
        return self.commence_query_row_set.GetRowID(row_index)

    def get_shared(self, row_index):
        return self.commence_query_row_set.GetShared(row_index)

    def get_field_to_file(self, row_index, column_index, file_path):
        return self.commence_query_row_set.GetFieldToFile(row_index, column_index, file_path)
