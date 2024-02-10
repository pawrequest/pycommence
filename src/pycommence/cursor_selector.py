from win32com.universal import com_error

from pycommence.entities import CmcError, Connection


class CursorSelector:

    def edit_record(self, record: str, package: dict):
        self._filter_by_name(record)
        row_set = self.get_edit_row_set()
        for key, value in package.items():
            try:
                col_idx = row_set.get_column_index(key)
                row_set.modify_row(0, col_idx, str(value))
            except Exception:
                raise CmcError(f'Could not modify {key} to {value}')
        row_set.commit()

    def get_record(self, record_name: str) -> list[dict[str, str]]:
        res = self._filter_by_name(record_name)
        if not res:
            raise CmcError(f'Could not find {record_name}')
        row_set = self.get_query_row_set()
        record = row_set.get_rows_dict()
        return record

    def delete_record(self, record_name: str) -> bool:
        try:
            res = self._filter_by_name(record_name)
            row_set = self.get_delete_row_set()
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
            row_set = self.get_add_row_set(1)
            row_set.modify_row(0, 0, record_name)
            row_set.modify_row_dict(0, package)
            res = row_set.commit()
            return res

        except com_error as e:
            # todo this is horrible. the error is due to threading but we are not using threading?
            # maybe pywin32 uses threading when handling the underlying db error?
            if e.hresult == -2147483617:
                raise CmcError('Record already exists')

    def _filter_by_field(self, field_name: str, condition, value=None, fslot=1):
        # filter_str = f'[ViewFilter(1, F,, "{field_name}", "{condition}", "{value})]'
        val_cond = f', "{value}"' if value else ''
        filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
        res = self.set_filter(filter_str)
        return res

    def _filter_by_connection(self, item_name: str, connection: Connection, fslot=1):
        filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                      f'{connection.to_table}, {item_name})]')
        res = self.set_filter(filter_str)
        if not res:
            raise ValueError(f'Could not set filter for ' f'{connection.name} = {item_name}')
        # todo return

    def _filter_by_name(self, name: str, fslot=1):
        res = self._filter_by_field('Name', 'Equal To', name, fslot=fslot)
        return res

    # def filter_by_date(
    #         cursor: ICommenceCursor,
    #         field_name: str,
    #         date: datetime.date,
    #         condition='After',
    # ):
    #     filter_str = f'[ViewFilter(1, F,, {field_name}, {condition}, {date})]'  # noqa E231
    #     res = cursor.SetFilter(filter_str, 0)
    #     return res
