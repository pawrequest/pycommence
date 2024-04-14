import typing as _t

import pydantic as _p

from . import cursor, pycmc_types


class PyCommence(_p.BaseModel):
    """
    Main interface for interacting with Commence.

    This class provides a high-level interface for managing records in a Commence database table,
    including creating, reading, updating, and deleting records.

    Args:
        csr: A :class:`cursor.Csr` object, best obtained via the `from_table_name` class method.

    Examples:
        Establish context

        >>> JEFF_KEY = 'JeffJones'
        >>> GEOFF_KEY = 'GeoffSmith'
        >>> GEOFF_DICT = {'firstName': 'Geoff', 'lastName': 'Smith', 'email': 'geoff@example.com'}
        >>> UPDATE_PKG = {'email': 'geoff.updated@example.com'}

        Instantiate a PyCommence object from table name

        >>> cmc = PyCommence.from_table_name('Contact')

        Get all records in the cursor

        >>> records = cmc.records()
        >>> print(records)
        [{'firstName': 'Jeff', 'lastName': 'Jones', ...}, {...}]

        Get a single record by primary key

        >>> print(cmc.one_record(JEFF_KEY))
        {'firstName': 'Jeff', 'lastName': 'Jones', 'email': 'jeff@example.com'}

        Add a new record

        >>> cmc.add_record(pk_val=GEOFF_KEY, package=GEOFF_DICT)
        True

        Modify a record

        >>> cmc.edit_record(pk_val=GEOFF_KEY, package=UPDATE_PKG)
        True

        Verify the updated record

        >>> updated_geoff = cmc.one_record(GEOFF_KEY)
        >>> print(updated_geoff['email'])
        'geoff.updated@example.com'

        Delete a record

        >>> cmc.delete_record(pk_val=GEOFF_KEY)
        True

    """
    csr: cursor.Csr

    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_table_name(cls, table_name: str, cmc_name: str = 'Commence.DB') -> 'PyCommence':
        return cls(csr=cursor.get_csr(table_name, cmc_name))

    def records(self, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        row_set = self.csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(self, pk_val: str) -> dict[str, str]:
        """Return a single record from the cursor by primary key."""
        with self.csr.temporary_filter_pk(pk_val):
            return self.records()[0]

    def records_by_field(
            self, field_name: str,
            value: str,
            max_rtn: int | None = None,
            empty: _t.Literal['ignore', 'raise'] = 'raise'
    ) -> list[dict[str, str]]:
        """
        Get records from the cursor by field name and value.

        Args:
            field_name: Name of the field to query.
            value: Value to filter by.
            max_rtn: Maximum number of records to return. If more than this, raise CmcError.
            empty: Action to take if no records are found. Options are 'ignore', 'raise'.

        Returns:
            A list of dictionaries of field names and values for the record.

        Raises:
            CmcError:
                - If the record is not found without slecting empty='ignore',
                - If max return is not None and more than max_rtn records are found.

        """
        with self.csr.temporary_filter_fields(field_name, 'Equal To', value, empty=empty):
            records = self.records()
            if not records and empty == 'raise':
                raise pycmc_types.CmcError(f'No record found for {field_name} {value}')
            if max_rtn and len(records) > max_rtn:
                raise pycmc_types.CmcError(f'Expected max {max_rtn} records, got {len(records)}')
            return records

    def edit_record(
            self,
            pk_val: str,
            package: dict,
    ) -> bool:
        """
        Modify a record.

        Args:
            pk_val (str): The value for the primary key field.
            package (dict): A dictionary of field names and values to modify.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val):
            row_set = self.csr.get_edit_rowset()
            row_set.modify_row_dict(0, package)
            return row_set.commit()

    def delete_record(self, pk_val: str, empty: pycmc_types.EmptyKind = 'raise'):
        """
        Delete a record.

        Args:
            pk_val (str): The value for the primary key field.
            empty (str): Action to take if the record is not found. Options are 'ignore', 'raise'.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val, empty=empty):  # noqa: PyArgumentList
            if self.csr.row_count == 0 and empty == 'ignore':
                return
            row_set = self.csr.get_delete_rowset(1)
            row_set.delete_row(0)
            res = row_set.commit()
            return res

    def delete_multiple(
            self,
            *,
            pk_vals: list[str],
            max_delete: int | None = 1,
            empty: pycmc_types.EmptyKind = 'raise'
    ):
        """
        Delete multiple records.

        Args:
            pk_vals (list): A list of primary key values.
            empty (str): Action to take if a record is not found. Options are 'ignore', 'raise'.
            max_delete (int): Maximum number of records to delete. If less than the number of records to delete, raise CmcError. Set None to disabl safety check

        Returns:
            bool: True on success

        """
        if max_delete and len(pk_vals) > max_delete:
            raise pycmc_types.CmcError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(pk_val, empty=empty)

    def add_record(
            self,
            pk_val: str,
            package: dict[str, str],
            existing: _t.Literal['replace', 'update', 'raise'] = 'raise'
    ) -> bool:
        """
        Add a record.

        Args:
            pk_val: The value for the primary key field.
            package: A dictionary of field names and values to add to the record.
            existing: Action to take if the record already exists. Options are 'replace', 'update', 'raise'.

        Returns:
            bool: True on success

        """
        with self.csr.temporary_filter_pk(pk_val, empty='ignore'):  # noqa: PyArgumentList
            if not self.csr.row_count:
                row_set = self.csr.get_named_addset(pk_val)
            else:
                if existing == 'raise':
                    raise pycmc_types.CmcError('Record already exists')
                elif existing == 'update':
                    row_set = self.csr.get_edit_rowset()
                elif existing == 'replace':
                    self.delete_record(pk_val)
                    row_set = self.csr.get_named_addset(pk_val)

            row_set.modify_row_dict(0, package)
            res = row_set.commit()
            return res
