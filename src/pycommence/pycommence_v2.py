import contextlib
import typing as _t
from functools import wraps

import pydantic as _p
from loguru import logger
from pydantic import Field

from pycommence.cursor import CursorAPI

# from pycommence import cursor
from pycommence.exceptions import PyCommenceExistsError, PyCommenceMaxExceededError, PyCommenceNotFoundError
from pycommence.pycmc_types import CmcFilter, FilterArray, NoneFoundHandler
from pycommence.wrapper.cmc_db import CommenceWrapper
from pycommence.wrapper.conversation import ConversationAPI, ConversationTopic
from pycommence.wrapper.enums_cmc import CursorType


def csr_f_tblname(func):
    @wraps(func)
    def wrapper(self, tblname: str, *args, **kwargs):
        tblname = kwargs.get('csrname')
        csr = self.get_csr(tblname)
        return func(self, csr=csr, *args, **kwargs)

    return wrapper


def with_csr2(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if 'csrname' in kwargs:
            tblname = kwargs['csrname']
        else:
            raise ValueError('csrname parameter is required')

        csr = self.get_csr(tblname)
        return func(self, csr=csr, *args, **kwargs)

    return wrapper


def filter_array_pk(pk_label, pk_val):
    return FilterArray.from_filters(CmcFilter(cmc_col=pk_label, value=pk_val))


class PyCommence(_p.BaseModel):
    cmc_wrapper: CommenceWrapper = Field(default_factory=CommenceWrapper)
    csrs: dict[str, CursorAPI] = Field(default_factory=dict)
    conversations: dict[ConversationTopic, ConversationAPI] = Field(default_factory=dict)
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    # @model_validator(mode='after')
    # def init_cmc(self):
    #     self.cmc_wrapper = self.cmc_wrapper or CommenceWrapper()
    #     return self

    def get_csr(self, csrname: str | None = None) -> CursorAPI:
        csrname = self.get_csrname(csrname)
        return self.csrs[csrname]

    def set_conversation(self, topic: ConversationTopic = 'ViewData'):
        self.conversations[topic] = self.cmc_wrapper.get_conversation_api(topic)
        return self

    def set_csr(
        self,
        csrname: str,
        mode: CursorType = CursorType.CATEGORY,
    ):
        cursor_wrapper = self.cmc_wrapper.get_new_cursor(csrname, mode=mode)
        cursor_api = CursorAPI(cursor_wrapper, db_name=self.cmc_wrapper.name, mode=mode, name=csrname)
        self.csrs[csrname] = cursor_api
        logger.debug(f'Set cursor on {csrname}')
        return self

    def reset_csr(self, csr):
        cursor_wrapper = self.cmc_wrapper.get_new_cursor(csr.name, mode=csr.mode)
        cursor_api = CursorAPI(cursor_wrapper, db_name=self.cmc_wrapper.name, mode=csr.mode, name=csr.name)
        self.csrs[cursor_api.name] = cursor_api
        logger.debug(f'Reset cursor on {csr.name}')

    def get_csrname(self, csrname):
        if not csrname:
            if not self.csrs:
                raise PyCommenceNotFoundError('No cursor available')
            if len(self.csrs) > 1:
                raise ValueError('Multiple cursors available, specify csrname')
            csrname = next(iter(self.csrs.keys()))
            logger.debug(f'Using cursorname {csrname}')
        return csrname

    def filter_cursor(self, filter_array: FilterArray, csrname: str | None = None) -> _t.Self:
        csr = self.get_csr(csrname)
        csr.filter_by_array(filter_array)
        return self

    def clear_csr_filters(self, tblname: str):
        csr = self.get_csr(tblname)
        csr.clear_all_filters()
        return self

    @contextlib.contextmanager
    def temporary_filter_cursor(self, filter_array: FilterArray, csrname: str | None = None) -> _t.Iterator[CursorAPI]:
        csr = self.get_csr(csrname)
        csr.filter_by_array(filter_array)
        yield csr
        csr.clear_all_filters()

    @classmethod
    def with_conversation(cls, topic: ConversationTopic = 'ViewData'):
        pyc = cls(cmc_wrapper=CommenceWrapper()).set_conversation(topic)
        return pyc

    @classmethod
    def with_csr(
        cls,
        csrname: str,
        filter_array: FilterArray | None = None,
        mode: CursorType = CursorType.CATEGORY,
    ):
        logger.debug(f'Creating PyCommence with cursor {csrname}')
        pyc = cls(cmc_wrapper=CommenceWrapper()).set_csr(csrname, mode=mode)
        if filter_array:
            pyc.filter_cursor(filter_array, csrname)
        logger.debug(f'Created PyCommence with cursor {csrname}{f" and filter {filter_array}" if filter_array else ""}')
        return pyc

    def generate_records(
        self, csrname: str | None = None, count: int | None = None
    ) -> _t.Generator[dict[str, str], None, None]:
        """Return all or first `count` records from the cursor."""
        csr = self.get_csr(csrname)
        row_set = csr.get_query_rowset(count)
        yield from row_set.gen_row_dicts()

    def generate_records_ids(
        self, *, csrname: str | None = None, count: int | None = None
    ) -> _t.Generator[dict[str, str], None, None]:
        """Return all or first `count` records from the cursor."""
        csr = self.get_csr(csrname)
        row_set = csr.get_query_rowset(count)
        yield from row_set.gen_rows_with_id()

    def records(self, csrname: str | None = None, count: int or None = None) -> list[dict[str, str]]:
        """Return all or first `count` records from the cursor."""
        csr = self.get_csr(csrname)
        row_set = csr.get_query_rowset(count)
        records = row_set.get_row_dicts()
        return records

    def one_record(
        self,
        pk_val: str,
        csrname: str | None = None,
    ) -> dict[str, str] | None:
        """Return a single record from the cursor by primary key."""
        csr = self.get_csr(csrname)

        with csr.temporary_filter_by_array(filter_array_pk(csr.pk_label, pk_val)):
            if csr.row_count == 0:
                raise PyCommenceNotFoundError(f'No record found for primary key {pk_val}')
            elif csr.row_count > 1:
                raise PyCommenceMaxExceededError(f'Multiple records found for primary key {pk_val}')
            return self.records(csr.name)[0]

    def records_by_array(
        self,
        filter_array: FilterArray,
        count: int | None = None,
        tblname: str | None = None,
    ) -> list[dict[str, str]]:
        csr = self.get_csr(tblname)
        with csr.temporary_filter_by_array(filter_array):
            return self.records(tblname, count)

    def edit_record(
        self,
        pk_val: str,
        row_dict: dict,
        tblname: str | None = None,
    ) -> _t.Self:
        """Edit a record in the cursor, fetch new cursor when done"""
        csr = self.get_csr(tblname)

        csr.filter_by_pk(pk_val, none_found=NoneFoundHandler.error)
        row_set = csr.get_edit_rowset()
        row_set.modify_row_dict(0, row_dict)
        row_set.commit()
        logger.debug(f'Edited record with primary key {pk_val}')
        self.reset_csr(csr)
        # self.reset_csr(csr.category)
        return self

    def delete_record(
        self,
        *,
        pk_val: str,
        none_found: NoneFoundHandler = 'raise',
        csrname: str | None = None,
    ) -> _t.Self:
        csr = self.get_csr(csrname)

        csr.filter_by_pk(pk_val, none_found=none_found)
        row_set = csr.get_delete_rowset(1)
        row_set.delete_row(0)
        row_set.commit()
        logger.debug(f'Deleted record with primary key {pk_val}')
        self.reset_csr(csr)
        # self.set_csr(csr.category)
        return self

    def delete_multiple(
        self,
        *,
        pk_vals: list[str],
        max_delete: int | None = 1,
        empty: NoneFoundHandler = 'raise',
        tblname: str | None = None,
    ) -> _t.Self:
        if max_delete and len(pk_vals) > max_delete:
            raise PyCommenceMaxExceededError(
                f'max_delete ({max_delete}) is less than the number of records to delete ({len(pk_vals)})'
            )
        for pk_val in pk_vals:
            self.delete_record(pk_val=pk_val, none_found=empty, csrname=tblname)
        return self

    def add_record(
        self,
        pk_val: str,
        row_dict: dict[str, str],
        tblname: str | None = None,
    ) -> _t.Self:
        csr = self.get_csr(tblname)

        if csr.pk_exists(pk_val):
            raise PyCommenceExistsError(f'Record with primary key {pk_val} already exists')
        else:
            row_set = csr.get_named_addset(pk_val)

        if row_set.row_count != 1:
            raise ValueError('RowSetAdd should have one row')

        row_set.modify_row_dict(0, row_dict)
        row_set.commit()
        logger.debug(f'Added record with primary key {pk_val}')
        self.reset_csr(csr)
        return self

        # with csr.temporary_filter_pk(pk_val, none_found=NoneFoundHandler.ignore):
        #     if not csr.row_count:
        #         row_set = csr.get_named_addset(pk_val)
        #     else:
        #         if existing == 'raise':
        #             raise PyCommenceExistsError()
        #         elif existing == 'update':
        #             row_set = csr.get_edit_rowset()
        #         elif existing == 'replace':
        #             self.delete_record(csrname=csrname, pk_val=pk_val)
        #             row_set = csr.get_named_addset(pk_val)

    def handle_existing(self, csr, existing, pk_val, tblname):
        match existing:
            case 'raise':
                raise PyCommenceExistsError()
            case 'update':
                row_set = csr.get_edit_rowset()
                logger.debug(f'Updating record with primary key {pk_val}')
            case 'replace':
                self.delete_record(pk_val=pk_val, csrname=tblname)
                row_set = csr.get_named_addset(pk_val)
                logger.debug(f'Replacing record with primary key {pk_val}')
            case _:
                raise ValueError(f'Invalid value for existing: {existing}')
        return row_set


def handle_none(none_found: NoneFoundHandler):
    match none_found:
        case NoneFoundHandler.error:
            raise PyCommenceNotFoundError()
        case NoneFoundHandler.ignore:
            return


def handle_multiple(count: int):
    ...
