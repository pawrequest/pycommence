import contextlib
import typing as _t

import pydantic as _p
from pydantic import Field, field_validator

from . import cursor, pycmc_types
from .cursor import CursorAPI, csr_context
from .pycmc_types import FilterArray
from .wrapper.cmc_db import CommenceWrapper


# def init_logging(external_logger=None):
#     print(f'intialising logger with {external_logger}')
#     configure_logging(external_logger)


class PyCommence(_p.BaseModel):
    # csr: CursorAPI | None = None
    cmc_wrapper: CommenceWrapper | None = None
    csrs: dict[str, CursorAPI] = Field(default_factory=dict)
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator('cmc_wrapper')
    def val_cmc(cls, v, values):
        return v or CommenceWrapper()

    def add_csr(self, tblname: str):
        self.csrs[tblname] = cursor.get_csr(tblname)

    @contextlib.contextmanager
    def with_csr(self, tblname: str) -> CursorAPI:
        csr = self.csrs.get(tblname)
        if not csr:
            self.add_csr(tblname)
        try:
            yield self.csrs.get(tblname)
        finally:
            ...

    # @property
    # def row_count(self) -> int:
    #     return self.csr.row_count

    # @classmethod
    # @contextlib.contextmanager
    # def from_table_name_context(
    #         cls,
    #         table_name: str,
    #         cmc_name: str = 'Commence.DB',
    #         filter_array: FilterArray | None = None,
    # ) -> 'PyCommence':
    #     """Context manager for :meth:`from_table_name`."""
    #     with csr_context(table_name, cmc_name, filter_array=filter_array) as csr:
    #         yield cls(csr=csr)

    def records(self, csr: CursorAPI, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        row_set = csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(self, pk_val: str, csr: CursorAPI) -> dict[str, str]:
        """Return a single record from the cursor by primary key."""
        with csr.temporary_filter_pk(pk_val):
            try:
                return self.records()[0]
            except IndexError:
                raise pycmc_types.CmcError(f'No record found for primary key {pk_val}')

    def records_by_array(
        self, csr: CursorAPI, filter_array: FilterArray, count: int | None = None
    ) -> list[dict[str, str]]:
        """Return records from the cursor by filter array."""
        with csr.temporary_filter_by_array(filter_array):
            return self.records(csr, count)

    def records_by_field(
        self,
        csr: CursorAPI,
        field_name: str,
        value: str,
        max_rtn: int | None = None,
        empty: _t.Literal['ignore', 'raise'] = 'raise',
    ) -> list[dict[str, str]]:
        with csr.temporary_filter_fields(field_name, 'Equal To', value, none_found=empty):
            records = self.records(csr)
            if not records and empty == 'raise':
                raise pycmc_types.CmcError(f'No record found for {field_name} {value}')
            if max_rtn and len(records) > max_rtn:
                raise pycmc_types.CmcError(f'Expected max {max_rtn} records, got {len(records)}')
            return records

    def edit_record(self, pk_val: str, row_dict: dict, csr: CursorAPI) -> bool:
        """
        Modify a record.

        Args:
            pk_val (str): The value for the primary key field.
            row_dict (dict): A dictionary of field names and values to modify.

        Returns:
            bool: True on success

        """
        with csr.temporary_filter_pk(pk_val):
            row_set = csr.get_edit_rowset()
            row_set.modify_row_dict(0, row_dict)
            return row_set.commit()

    def delete_record(self, csr: CursorAPI, pk_val: str, empty: pycmc_types.EmptyKind = 'raise'):
        """
        Delete a record.

        Args:
            pk_val (str): The value for the primary key field.
            empty (str): Action to take if the record is not found. Options are 'ignore', 'raise'.

        Returns:
            bool: True on success

        """
        with csr.temporary_filter_pk(pk_val, none_found=empty):  # noqa: PyArgumentList
            if csr.row_count == 0 and empty == 'ignore':
                return
            row_set = csr.get_delete_rowset(1)
            row_set.delete_row(0)
            res = row_set.commit()
            return res

    def delete_multiple(
        self, *, csr: CursorAPI, pk_vals: list[str], max_delete: int | None = 1, empty: pycmc_types.EmptyKind = 'raise'
    ):
        if max_delete and len(pk_vals) > max_delete:
            raise pycmc_types.CmcError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(csr, pk_val, empty=empty)

    def add_record(
        self,
        csr: CursorAPI,
        pk_val: str,
        row_dict: dict[str, str],
        existing: _t.Literal['replace', 'update', 'raise'] = 'raise',
    ) -> bool:
        with csr.temporary_filter_pk(pk_val, none_found='ignore'):  # noqa: PyArgumentList
            if not csr.row_count:
                row_set = csr.get_named_addset(pk_val)
            else:
                if existing == 'raise':
                    raise pycmc_types.CmcError('Record already exists')
                elif existing == 'update':
                    row_set = csr.get_edit_rowset()
                elif existing == 'replace':
                    self.delete_record(csr, pk_val)
                    row_set = csr.get_named_addset(pk_val)

            row_set.modify_row_dict(0, row_dict)
            res = row_set.commit()
            return res
