import contextlib
import typing as _t

import pydantic as _p
from comtypes import CoInitialize, CoUninitialize
from loguru import logger
from pydantic import Field

from pycommence.cursor_v2 import CursorAPI, raise_for_id_or_pk
from pycommence.exceptions import PyCommenceNotFoundError
from pycommence.filters import FilterArray
from pycommence.pycmc_types import CursorType, MoreAvailable, Pagination, RowFilter
from pycommence.wrapper.cmc_wrapper import CommenceWrapper
from pycommence.wrapper.conversation_wrapper import ConversationAPI, ConversationTopic


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
    ) -> _t.Self:
        """Re/Set the cursor by name and values"""
        cursor = self.cmc_wrapper.get_new_cursor(csrname, mode)
        self.csrs[csrname] = cursor
        # logger.debug(f'Set "{csrname}" ({mode.name.title()}) cursor with {cursor.row_count} rows')
        return self

    def get_csrname(self, csrname: str | None = None):
        if not csrname:
            if not self.csrs:
                raise PyCommenceNotFoundError('No cursor available')
            if len(self.csrs) > 1:
                raise ValueError('Multiple cursors available, specify csrname')
            csrname = next(iter(self.csrs.keys()))
            # logger.debug(f'Using cursorname {csrname}')
        return csrname

    def csr(self, csrname: str | None = None) -> CursorAPI:
        """Return a cursor by name, or the only cursor if only one is available."""
        csrname = self.get_csrname(csrname)
        return self.csrs[csrname]

    def refresh_csr(self, csr) -> _t.Self:
        """Reset an existing cursor with same name, mode and filter_array"""
        self.set_csr(csr.csrname, csr.mode)
        logger.debug(f'Refreshed cursor on {csr.csrname} with {csr.row_count} rows')
        return self

    @classmethod
    def with_csr(
        cls,
        csrname: str,
        mode: CursorType = CursorType.CATEGORY,
    ):
        return cls().set_csr(csrname, mode=mode)

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
        row_id: str | None = None,  # id or pk must be provided
        pk: str | None = None,
        with_category: bool = False,
    ) -> dict[str, str]:
        csr = self.csr(csrname)
        return csr._read_row(row_id=row_id, pk=pk, with_category=with_category)

    def read_rows(
        self,
        csrname: str | None = None,
        pagination: Pagination | None = None,
        filter_array: FilterArray | None = None,
        row_filter: RowFilter | None = None,
    ) -> _t.Generator[dict[str, str] | MoreAvailable, None, None]:
        """
        Generate rows from a cursor
        Args:
            csrname: Name of cursor
            pagination: Pagination object
            filter_array: FilterArray object (override cursor filter)
            row_filter: Filter generator

        Yields:
            dict: Row data or MoreAvailable object
        """
        logger.debug(f'Reading rows from {csrname}: {filter_array} | {pagination}')
        yield from self.csr(csrname)._read_rows(
            pagination=pagination,
            filter_array=filter_array,
            row_filter=row_filter,
        )

    def update_row(
        self, update_pkg: dict, row_id: str | None = None, pk: str | None = None, csrname: str | None = None
    ):
        """Update a row by id or pk

        Args:
            update_pkg: dict of field names and values to update
            row_id: row id (id or pk must be provided)
            pk: row pk (id or pk must be provided)
            csrname: cursor name (default = Self.get_csrname())

        """
        raise_for_id_or_pk(row_id, pk)
        csr = self.csr(csrname)
        row_id = row_id or csr.pk_to_id(pk)
        csr._update_row(update_pkg, id=row_id)
        self.refresh_csr(csr)

    def delete_row(self, row_id: str | None = None, pk: str | None = None, csrname: str | None = None):
        raise_for_id_or_pk(row_id, pk)
        csr = self.csr(csrname)
        row_id = row_id or csr.pk_to_id(pk)
        row = self.read_row(csrname=csr.category, row_id=row_id)
        csr._delete_row(id=row_id)
        self.refresh_csr(csr)


@contextlib.contextmanager
def pycommence_context(csrname: str, mode: CursorType = CursorType.CATEGORY) -> PyCommence:
    CoInitialize()
    pyc = PyCommence.with_csr(csrname, mode=mode)
    yield pyc
    CoUninitialize()


@contextlib.contextmanager
def pycommences_context(csrnames: list[str]) -> PyCommence:
    CoInitialize()
    pyc = PyCommence()
    for csrname in csrnames:
        pyc.set_csr(csrname)
    yield pyc
    CoUninitialize()
