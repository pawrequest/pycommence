import typing as _t
from functools import wraps

import pydantic as _p
from loguru import logger
from pydantic import Field

from pycommence.cursor_v2 import CursorAPI
# from pycommence import cursor
from pycommence.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.pycmc_types import CursorType
from pycommence.filters import CmcFilter, FilterArray
from pycommence.wrapper.cmc_wrapper import CommenceWrapper
from pycommence.wrapper.conversation_wrapper import ConversationAPI, ConversationTopic
from pycommence.wrapper.cursor_wrapper import CursorWrapper


def csr_f_tblname(func):
    @wraps(func)
    def wrapper(self, tblname: str, *args, **kwargs):
        tblname = kwargs.get('csrname')
        csr = self.csr(tblname)
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

    # cursor ops:
    def get_new_cursor(self, csrname, mode, filter_array=None) -> CursorAPI:
        """Create a new cursor with the specified name and mode."""
        cursor_wrapper: CursorWrapper = self.cmc_wrapper.get_new_cursor(csrname, mode=mode)
        return CursorAPI(cursor_wrapper, mode=mode, csrname=csrname, filter_array=filter_array)

    def csr(self, csrname: str | None = None) -> CursorAPI:
        """ Return a cursor by name, or the only cursor if only one is available."""
        csrname = self.get_csrname(csrname)
        return self.csrs[csrname]

    def set_csr(
            self,
            csrname: str,
            mode: CursorType = CursorType.CATEGORY,
            filter_array: FilterArray | None = None,
    ) -> _t.Self:
        self.csrs[csrname] = self.get_new_cursor(csrname, mode, filter_array)
        logger.debug(f'Set cursor on {csrname}')
        return self

    def get_csrname(self, csrname):
        if not csrname:
            if not self.csrs:
                raise PyCommenceNotFoundError('No cursor available')
            if len(self.csrs) > 1:
                raise ValueError('Multiple cursors available, specify csrname')
            csrname = next(iter(self.csrs.keys()))
            logger.debug(f'Using cursorname {csrname}')
        return csrname

    @classmethod
    def with_csr(
            cls,
            csrname: str,
            filter_array: FilterArray | None = None,
            mode: CursorType = CursorType.CATEGORY,
    ):
        pyc = cls()
        pyc.set_csr(csrname, mode=mode, filter_array=filter_array)
        logger.debug(f'Created PyCommence with cursor {csrname}{f" and filter {filter_array}" if filter_array else ""}')
        return pyc

    def set_conversation(self, topic: ConversationTopic = 'ViewData'):
        self.conversations[topic] = self.cmc_wrapper.get_conversation_api(topic)
        return self

    @classmethod
    def with_conversation(cls, topic: ConversationTopic = 'ViewData'):
        return cls(cmc_wrapper=CommenceWrapper()).set_conversation(topic)


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
