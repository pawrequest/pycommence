import contextlib
import typing as _t
from functools import wraps

import pydantic as _p
from pydantic import Field, model_validator

import pycommence.exceptions
from . import PyCommenceExistsError, PyCommenceNotFoundError, cursor, pycmc_types
from .cursor import CursorAPI
from .pycmc_types import (
    FilterArray,
    NoneFoundHandler,
)
from .exceptions import PyCommenceMaxExceededError
from .wrapper.cmc_db import CommenceWrapper
from .wrapper.enums_cmc import CursorType


def csr_f_tblname(func):
    @wraps(func)
    def wrapper(self, tblname: str, *args, **kwargs):
        tblname = kwargs.get('tblname')
        csr = self.get_csr(tblname)
        return func(self, csr=csr, *args, **kwargs)

    return wrapper


def with_csr2(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'tblname' in kwargs:
            tblname = kwargs['tblname']
        else:
            raise ValueError('tblname parameter is required')

        csr = self.get_csr(tblname)
        return func(self, csr=csr, *args, **kwargs)

    return wrapper


class PyCommence(_p.BaseModel):
    cmc_wrapper: CommenceWrapper | None = None
    csrs: dict[str, CursorAPI] = Field(default_factory=dict)
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    # @field_validator('cmc_wrapper', mode='after')
    # def init_cmc(cls, v, values):
    #     return v if v is not None else CommenceWrapper()

    @model_validator(mode='after')
    def init_cmc2(self):
        self.cmc_wrapper = self.cmc_wrapper or CommenceWrapper()
        return self

    def get_csr(self, tblname: str | None = None) -> CursorAPI:
        if tblname:
            return self.csrs[tblname]
        if self.csrs:
            return next(iter(self.csrs.values()))
        raise PyCommenceNotFoundError('No cursor available')

    def set_csr(
            self, tblname: str,
            mode: CursorType = CursorType.CATEGORY,
    ):
        if not tblname:
            raise ValueError('tblname parameter is required')
        self.csrs[tblname] = cursor.get_csr(tblname, mode=mode)
        return self

    def filter_cursor(self, tblname: str, filter_array: FilterArray) -> _t.Self:
        # csr = self.csrs[tblname]
        csr = self.get_csr(tblname)
        csr.filter_by_array(filter_array)
        return self

    def clear_csr_filters(self, tblname: str):
        csr = self.get_csr(tblname)
        csr.clear_all_filters()
        return self

    @contextlib.contextmanager
    def temporary_filter_cursor(self, filter_array: FilterArray, tblname: str | None = None) -> _t.Iterator[CursorAPI]:
        csr = self.get_csr(tblname)
        csr.filter_by_array(filter_array)
        yield csr
        csr.clear_all_filters()

    @classmethod
    def with_csr(
            cls, tblname: str, filter_array: FilterArray | None = None,
            mode: CursorType = CursorType.CATEGORY,
    ):
        pyc = cls(cmc_wrapper=CommenceWrapper()).set_csr(tblname, mode=mode)
        if filter_array:
            pyc.filter_cursor(tblname, filter_array)
        return pyc

    def records(self, tblname: str | None = None, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        csr = self.get_csr(tblname)
        row_set = csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(self, pk_val: str, tblname: str | None = None) -> dict[str, str]:
        """Return a single record from the cursor by primary key."""
        csr = self.get_csr(tblname)

        with csr.temporary_filter_pk(pk_val):
            if csr.row_count == 0:
                raise PyCommenceNotFoundError(f'No record found for primary key {pk_val}')
            elif csr.row_count > 1:
                raise PyCommenceMaxExceededError(f'Multiple records found for primary key {pk_val}')
            try:
                return self.records(tblname)[0]
            except IndexError:
                raise pycommence.exceptions.PyCommenceNotFoundError(f'No record found for primary key {pk_val}')

    def records_by_array(
            self,
            filter_array: FilterArray,
            count: int | None = None,
            tblname: str | None = None,
    ) -> list[dict[str, str]]:
        # csr = self.csrs[tblname]
        csr = self.get_csr(tblname)

        with csr.temporary_filter_by_array(filter_array):
            return self.records(tblname, count)

    def edit_record(
            self,
            pk_val: str,
            row_dict: dict,
            tblname: str | None = None,
    ) -> _t.Self:
        csr = self.get_csr(tblname)

        csr.filter_by_pk(pk_val, none_found=NoneFoundHandler.error)
        row_set = csr.get_edit_rowset()
        row_set.modify_row_dict(0, row_dict)
        row_set.commit()
        self.set_csr(csr.category)
        return self

    def delete_record(
            self,
            *,
            pk_val: str,
            empty: pycmc_types.EmptyKind = 'raise',
            tblname: str | None = None,
    ) -> _t.Self:
        csr = self.get_csr(tblname)

        with csr.temporary_filter_pk(pk_val, none_found=empty):  # noqa: PyArgumentList
            if csr.row_count == 0 and empty == 'ignore':
                return
            row_set = csr.get_delete_rowset(1)
            row_set.delete_row(0)
            row_set.commit()
            self.set_csr(csr.category)
            return self

    def delete_multiple(
            self,
            *,
            pk_vals: list[str],
            max_delete: int | None = 1,
            empty: pycmc_types.EmptyKind = 'raise',
            tblname: str | None = None,
    ) -> _t.Self:
        if max_delete and len(pk_vals) > max_delete:
            raise pycommence.exceptions.CmcError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(pk_val=pk_val, empty=empty, tblname=tblname)
        return self

    def add_record(
            self,
            pk_val: str,
            row_dict: dict[str, str],
            existing: _t.Literal['replace', 'update', 'raise'] = 'raise',
            tblname: str | None = None,
    ) -> _t.Self:
        csr = self.get_csr(tblname)

        with csr.temporary_filter_pk(pk_val, none_found=NoneFoundHandler.ignore):
            if not csr.row_count:
                row_set = csr.get_named_addset(pk_val)
            else:
                if existing == 'raise':
                    raise PyCommenceExistsError()
                elif existing == 'update':
                    row_set = csr.get_edit_rowset()
                elif existing == 'replace':
                    self.delete_record(tblname=tblname, pk_val=pk_val)
                    row_set = csr.get_named_addset(pk_val)

            row_set.modify_row_dict(0, row_dict)
            row_set.commit()
            self.set_csr(csr.category)
            return self
