import typing as _t
from dataclasses import dataclass, field

from loguru import logger

from pycommence.cursor import CursorAPI, RESULTS_GENERATOR2, raise_for_id_or_pk
from pycommence.filters import FilterArray
from pycommence.meta.meta import CommenceTable
from pycommence.meta.pycmc_fields import DELIM
from pycommence.pycmc_types import CursorType, RowFilter
from pycommence.pagination import Pagination
from pycommence.resolvers import resolve_csrname, resolve_row_id
from pycommence.wrapper.cmc_wrapper import CommenceWrapper
from pycommence.wrapper.conversation_wrapper import ConversationAPI, DDEKind, DDETopic


# noinspection PyProtectedMember
@dataclass
class PyCommence:
    """
    Main interface for interacting with a Commence database.

    Manages database connections, cursors, and DDE conversations.
    Provides high-level methods for CRUD operations and cursor management.
    Wraps an instance of :class:`~pycommence.wrapper.cmc_wrapper.CommenceWrapper`

    Typical Usage:
        >>> pyc = PyCommence.with_csr("Contacts", mode=CursorType.CATEGORY)
        >>> pyc.create_row({"Name": "Alice"})
        >>> for row in pyc.read_rows():
        ...     print(row)

    """

    cmc_wrapper: CommenceWrapper = field(default_factory=CommenceWrapper)
    csrs: dict[str, CursorAPI] = field(default_factory=dict)
    conversations: dict[DDETopic, ConversationAPI] = field(default_factory=dict)

    @classmethod
    def with_csr(
            cls,
            csrname: str,
            mode: CursorType = CursorType.CATEGORY,
    ):
        """
        Create a new PyCommence instance with a cursor.

        Args:
            csrname (str): Name of the category or view.
            mode (CursorType): Cursor type (default: CATEGORY).

        Returns:
            PyCommence: Instance with cursor initialised.
        """
        return cls().set_csr(csrname, mode=mode)

    @resolve_csrname
    def set_csr(
            self,
            csrname: str,
            mode: CursorType = CursorType.CATEGORY,
    ) -> _t.Self:
        """
        Add or update a cursor by name and type.

        Args:
            csrname (str): Name of the category or view.
            mode (CursorType): Cursor type (default: CATEGORY).

        Returns:
            PyCommence: Self for chaining.
        """
        cursor_wrapper = self.cmc_wrapper.establish_cursor(csrname, mode)
        cursor = CursorAPI(cursor_wrapper=cursor_wrapper, mode=mode)
        # cursor = self.cmc_wrapper.get_new_cursor(csrname, mode)
        self.csrs[csrname] = cursor
        logger.debug(f'Set "{csrname}" ({mode.name.title()}) cursor with {cursor.row_count} rows')
        return self

    @resolve_csrname
    def csr(self, csrname: str | None = None) -> CursorAPI:
        """Return a cursor by name, or the only cursor if only one is available."""
        # csrname = self.get_csrname(csrname)
        return self.csrs[csrname]

    def refresh_csr(self, csr: CursorAPI) -> _t.Self:
        """Reset an existing cursor with same name, mode and filter_array"""
        self.set_csr(csr.csrname, csr.mode)
        # logger.debug(f'Refreshed cursor on {csr.csrname} with {csr.row_count} rows')
        return self

    # def send_dde_obj(self, dde_command: DDEMessage):
    #     self.send_dde(topic=dde_command.topic, kind=dde_command.kind, cmd=dde_command.to_dde())

    def send_dde(self, cmd: str, topic: DDETopic = DDETopic.VIEW_DATA, kind: DDEKind = DDEKind.REQUEST):
        logger.debug(f'Sending DDE command to topic {topic} ({kind}): {cmd}/\nCOMAND_LENGTH = {len(cmd)}')
        conv = self.get_conversation(topic)
        res = conv.send_dde(cmd, kind)
        if isinstance(res, str) and DELIM in res:
            res = res.split(DELIM)
        return res

    def get_conversation(self, topic: DDETopic) -> ConversationAPI | None:
        conv = self.conversations.get(topic)
        if not conv:
            logger.debug(f'Establishing new conversation for topic: {topic}')
            self.conversations[topic] = self.cmc_wrapper.establish_conversation(topic)
            conv = self.conversations[topic]
        return conv

    def create_row(self, create_pkg: dict[str, str], csrname: str | None = None):
        """
        Add a new row to the database.

        Args:
            create_pkg (dict): Field names and values for the new row.
            csrname (str, optional): Cursor name (or only available).

        """
        csr = self.csr(csrname)
        csr.create_row(create_pkg)
        self.refresh_csr(csr)

    @resolve_row_id
    def read_row2(
            self,
            *,
            csrname: str | None = None,
            row_id: str | None = None,  # id or pk must be provided
            pk: str | None = None,
    ) -> CommenceTable:
        raise_for_id_or_pk(row_id, pk)
        csr = self.csr(csrname)
        return csr.read_row(row_id=row_id)


    def read_rows(
            self,
            csrname: str | None = None,
            pagination: Pagination | None = None,
            filter_array: FilterArray | None = None,
            row_filter: RowFilter | None = None,
            # fetch_ids: bool = True,
    ) -> RESULTS_GENERATOR2:
        """
        Generate rows from a cursor

        Args:
            csrname: Name of cursor (optional if only one cursor is set)
            pagination: Pagination object
            filter_array: FilterArray object (override cursor filter)
            row_filter: Filter generator
            fetch_ids: default: True, disable for performance

        Yields:
            row_data:RowData
            more_available: MoreAvailable
        """
        logger.debug(f'Reading rows from {csrname}: {filter_array} | {pagination}')
        yield from self.csr(csrname).read_rows(
            pagination=pagination,
            filter_array=filter_array,
            row_filter=row_filter,
        )

    @resolve_row_id
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
        csr.update_row(update_pkg, id=row_id)
        self.refresh_csr(csr)

    @resolve_row_id
    def delete_row(self, row_id: str | None = None, pk: str | None = None, csrname: str | None = None):
        """Delete a row by ID or primary key."""
        raise_for_id_or_pk(row_id, pk)
        csr = self.csr(csrname)
        self.read_row2(csrname=csr.category, row_id=row_id)  # Ensure the row exists before deleting
        csr.delete_row(id=row_id)
        self.refresh_csr(csr)
