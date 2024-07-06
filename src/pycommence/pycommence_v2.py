import typing as _t
from functools import wraps

import pydantic as _p
from loguru import logger
from pydantic import Field

from pycommence.cursor_v2 import CursorAPI, raise_for_id_or_pk
# from pycommence import cursor
from pycommence.exceptions import PyCommenceNotFoundError
from pycommence.filters import ConditionType, FieldFilter, FilterArray
from pycommence.pycmc_types import CursorType
from pycommence.wrapper.cmc_wrapper import CommenceWrapper
from pycommence.wrapper.conversation_wrapper import ConversationAPI, ConversationTopic


def csr_f_tblname(func):
    @wraps(func)
    def wrapper(self, tblname: str, *args, **kwargs):
        tblname = kwargs.get('csrname')
        csr = self.csr(tblname)
        return func(self, csr=csr, *args, **kwargs)

    return wrapper


def filter_array_pk(pk_label, pk_val):
    return FilterArray.from_filters(FieldFilter(column=pk_label, value=pk_val))


# noinspection PyProtectedMember
class PyCommence(_p.BaseModel):
    cmc_wrapper: CommenceWrapper = Field(default_factory=CommenceWrapper)
    csrs: dict[str, CursorAPI] = Field(default_factory=dict)
    conversations: dict[ConversationTopic, ConversationAPI] = Field(default_factory=dict)
    model_config = _p.ConfigDict(
        arbitrary_types_allowed=True,
    )

    def set_csr(
            self,
            csrname: str,
            mode: CursorType = CursorType.CATEGORY,
            filter_array: FilterArray | None = None,
    ) -> _t.Self:
        """Re/Set the cursor by name and values"""
        self.csrs[csrname] = self.cmc_wrapper.get_new_cursor(csrname, mode, filter_array)
        logger.debug(f'Set cursor on {csrname}')
        return self

    def get_csrname(self, csrname: str | None = None):
        if not csrname:
            if not self.csrs:
                raise PyCommenceNotFoundError('No cursor available')
            if len(self.csrs) > 1:
                raise ValueError('Multiple cursors available, specify csrname')
            csrname = next(iter(self.csrs.keys()))
            logger.debug(f'Using cursorname {csrname}')
        return csrname

    def csr(self, csrname: str | None = None) -> CursorAPI:
        """Return a cursor by name, or the only cursor if only one is available."""
        csrname = self.get_csrname(csrname)
        return self.csrs[csrname]

    def refresh_csr(self, csr) -> _t.Self:
        """Reset an existing cursor with same name, mode and filter_array"""
        self.set_csr(csr.csrname, csr.mode, csr.filter_array)
        return self

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

    def create_row(self, create_pkg: dict[str, str], csrname: str | None = None):
        csr = self.csr(csrname)
        csr._create_row(create_pkg)
        self.refresh_csr(csr)

    def read_row(
            self,
            *,
            csrname: str | None = None,
            id: str | None = None,
            pk: str | None = None,
            with_category: bool = False
    ) -> dict[str, str]:
        csr = self.csr(csrname)
        return csr._read_row(id=id, pk=pk, with_category=with_category)

    def read_rows(
            self,
            count: int | None = None,
            csrname: str | None = None,
            with_category: bool = True,
    ) -> _t.Generator[dict[str, str], None, None]:
        csr = self.csr(csrname)
        return csr._read_rows(count, with_category)

    def read_rows_pk_contains(
            self,
            pk: str,
            csrname: str | None = None,
            count: int | None = None,

    ) -> _t.Generator[dict[str, str], None, None]:
        csr = self.csr(csrname)
        yield from csr._read_rows_filtered(
            filter_array=csr.pk_filter(pk, condition=ConditionType.CONTAIN),
            count=count
        )

    def update_row(self, update_pkg: dict, id: str | None = None, pk: str | None = None, csrname: str | None = None):
        raise_for_id_or_pk(id, pk)
        csr = self.csr(csrname)
        id = id or csr.pk_to_id(pk)
        csr._update_row(update_pkg, id=id)
        self.refresh_csr(csr)

    def delete_row(self, id: str | None = None, pk: str | None = None, csrname: str | None = None):
        raise_for_id_or_pk(id, pk)
        csr = self.csr(csrname)
        id = id or csr.pk_to_id(pk)
        csr._delete_row(id=id)
        self.refresh_csr(csr)
