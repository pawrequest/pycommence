import contextlib
import typing as _t

import pydantic as _p
from pydantic import Field, field_validator

from . import cursor, pycmc_types
from .cursor import CursorAPI
from .pycmc_types import (
    FilterArray,
    NoneFoundHandler,
    PyCommenceExistsError,
    PyCommenceMaxExceededError,
    PyCommenceNotFoundError,
)
from .wrapper.cmc_db import CommenceWrapper


class PyCommence(_p.BaseModel):
    cmc_wrapper: CommenceWrapper | None = None
    csrs: dict[str, CursorAPI] = Field(default_factory=dict)
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator('cmc_wrapper')
    def val_cmc(cls, v, values):
        return v or CommenceWrapper()

    def set_csr(self, tblname: str):
        self.csrs[tblname] = cursor.get_csr(tblname)
        return self

    def filter_cursor(self, tblname: str, filter_array: FilterArray) -> _t.Self:
        csr = self.csrs[tblname]
        csr.filter_by_array(filter_array)
        return self

    def clear_csr_filters(self, tblname: str):
        csr = self.csrs[tblname]
        csr.clear_all_filters()
        return self

    @contextlib.contextmanager
    def temporary_filter_cursor(self, tblname: str, filter_array: FilterArray) -> _t.Iterator[CursorAPI]:
        csr = self.csrs[tblname]
        csr.filter_by_array(filter_array)
        yield csr
        csr.clear_all_filters()

    @classmethod
    def with_csr(cls, tblname: str, filter_array: FilterArray | None = None):
        pyc = cls(cmc_wrapper=CommenceWrapper()).set_csr(tblname)
        if filter_array:
            pyc.filter_cursor(tblname, filter_array)
        return pyc

    def records(self, tblname: str, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        csr = self.csrs[tblname]
        row_set = csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(self, tblname: str, pk_val: str) -> dict[str, str]:
        """Return a single record from the cursor by primary key."""
        csr = self.csrs[tblname]
        with csr.temporary_filter_pk(pk_val):
            if csr.row_count == 0:
                raise PyCommenceNotFoundError(f'No record found for primary key {pk_val}')
            elif csr.row_count > 1:
                raise PyCommenceMaxExceededError(f'Multiple records found for primary key {pk_val}')
            try:
                return self.records(tblname)[0]
            except IndexError:
                raise pycmc_types.PyCommenceNotFoundError(f'No record found for primary key {pk_val}')

    def records_by_array(
            self, tblname: str, filter_array: FilterArray, count: int | None = None
    ) -> list[dict[str, str]]:
        csr = self.csrs[tblname]
        with csr.temporary_filter_by_array(filter_array):
            return self.records(tblname, count)

    def edit_record(self, tblname: str, pk_val: str, row_dict: dict) -> _t.Self:
        csr = self.csrs[tblname]
        csr.filter_by_pk(pk_val, none_found=NoneFoundHandler.error)
        row_set = csr.get_edit_rowset()
        row_set.modify_row_dict(0, row_dict)
        row_set.commit()
        self.set_csr(tblname)
        return self

    def delete_record(self, tblname: str, pk_val: str, empty: pycmc_types.EmptyKind = 'raise') -> _t.Self:
        csr = self.csrs[tblname]
        with csr.temporary_filter_pk(pk_val, none_found=empty):  # noqa: PyArgumentList
            if csr.row_count == 0 and empty == 'ignore':
                return
            row_set = csr.get_delete_rowset(1)
            row_set.delete_row(0)
            row_set.commit()
            self.set_csr(tblname),
            return self

    def delete_multiple(
            self,
            *,
            tblname: str,
            pk_vals: list[str],
            max_delete: int | None = 1,
            empty: pycmc_types.EmptyKind = 'raise'
    ) -> _t.Self:
        if max_delete and len(pk_vals) > max_delete:
            raise pycmc_types.CmcError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(tblname, pk_val, empty=empty)
        return self

    def add_record(
            self,
            tblname: str,
            pk_val: str,
            row_dict: dict[str, str],
            existing: _t.Literal['replace', 'update', 'raise'] = 'raise',
    ) -> _t.Self:
        csr = self.csrs[tblname]
        with csr.temporary_filter_pk(pk_val, none_found=NoneFoundHandler.ignore):
            if not csr.row_count:
                row_set = csr.get_named_addset(pk_val)
            else:
                if existing == 'raise':
                    raise PyCommenceExistsError()
                elif existing == 'update':
                    row_set = csr.get_edit_rowset()
                elif existing == 'replace':
                    self.delete_record(tblname, pk_val)
                    row_set = csr.get_named_addset(pk_val)

            row_set.modify_row_dict(0, row_dict)
            row_set.commit()
            self.set_csr(tblname)
            return self
