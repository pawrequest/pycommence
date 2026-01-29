from __future__ import annotations

import typing as _t
from typing import cast

import pythoncom
from loguru import logger
from win32com.client import Dispatch
from win32com.universal import com_error

from pycommence.dde import DDETopic
from pycommence.core.exceptions import PyCommenceServerError
from pycommence.icommence.const import OptionFlag
from pycommence.icommence.const import CursorType
from pycommence.conversation import ConversationAPI
from pycommence.icommence.cursor_wrapper import CursorWrapper
from pycommence.icommence.db import ICommenceDB


class PyCommenceConnector:
    """Singleton managing cached connections to multiple Commence databases."""

    # _connections: dict[str, PyCommenceAPI] = {}

    # caching breaks multi-threaded
    # def __new__(cls, commence_instance_name: str = 'Commence.DB') -> PyCommenceConnector:
    #     if commence_instance_name in cls._connections:
    #         logger.info(f'Using cached connection to {commence_instance_name}')
    #     else:
    #         new__ = super().__new__(PyCommenceAPI)
    #         cls._connections[commence_instance_name] = new__
    #         logger.info(f'Created new connection to {commence_instance_name}')
    #
    #     return cls._connections[commence_instance_name]

    def __init__(self, commence_instance_name: str = 'Commence.DB'):
        self.commence_instance_name = commence_instance_name
        self.commence_app: ICommenceDB | None = None

    def _initialize_connection(self):
        """Initialize the COM connection to the Commence database."""

        com_inited = False
        try:
            try:
                pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
                com_inited = True

            except pythoncom.com_error as e:
                pass

            if self.commence_app is not None:
                return
            try:
                res = Dispatch(self.commence_instance_name)
                self.commence_app = cast(ICommenceDB, cast(object, res))
                logger.info(f'Connected to Commence instance: {self.commence_instance_name}')
            except com_error as e:
                error_msg = f'Error connecting to {self.commence_instance_name}: {str(e)}'
                logger.error(error_msg)
                raise PyCommenceServerError(error_msg) from e

        finally:
            if com_inited:
                pythoncom.CoUninitialize()

        logger.debug(f'Initializing COM connection to {self.commence_instance_name}')


class PyCommenceAPI(PyCommenceConnector):
    """Commence Database object.

    Entry point for :class:`.cmc_csr.CsrCmc` and :class:`.conversation.CommenceConversation`.

    ~~Caching Inherited from :class:`.PyCommenceConnector`.~~ caching breaks in multithreaded environments

    Attributes:
       commence_instance_name (str): The name of the Commence instance.
       commence_app (Dispatch): The Commence COM object.

    """

    # def get_new_cursor(self, csrname, mode=CursorType.CATEGORY) -> CursorAPI:
    #     """Create a new cursor with the specified name and mode."""
    #     cursor_wrapper: CursorWrapper = self._get_new_cursor_wrapper(csrname, mode=mode)
    #     return CursorAPI(cursor_wrapper, mode=mode, csrname=csrname)
    _name: str | None = None
    _path: str | None = None
    _registered_user: str | None = None
    _shared: bool | None = None
    _version: str | None = None
    _version_ext: str | None = None

    def establish_cursor(
            self,
            name: str | None = None,
            mode: CursorType = CursorType.CATEGORY,
            pilot: bool = False,
            internet: bool = False,
    ) -> CursorWrapper:
        """Create a cursor wrapper.

        CursorTypes CATEGORY and VIEW require name to be set.

        Args:
            name (str|None): Name of the category or view to open.
            mode (enums_cmc.CursorType): Cursor type
            pilot (bool): Pilot flag - use palmpilot preferences
            internet (bool): Internet flag - use internet preferences

        Returns:
            CsrCmc: A Csr object on success.

        Raises:
            ValueError if no name given for name based searches

        """
        self._initialize_connection()
        if pilot and internet:
            raise ValueError('Only one of pilot or internet can be set')
        if mode in [CursorType.CATEGORY, CursorType.VIEW] and not name:
            raise ValueError(f'{mode.name} cursor mode requires name param to be set')

        flags = OptionFlag.NONE
        if pilot:
            flags |= OptionFlag.PILOT
        if internet:
            flags |= OptionFlag.INTERNET

        try:
            csr = CursorWrapper(self.commence_app.GetCursor(mode.value, name, flags.value))
        except com_error as e:
            raise PyCommenceServerError(f'Error creating cursor for {name} in {self.name}: {e}')
        return csr
        # todo non-standard modes

    def establish_conversation(self, topic):
        application_name = 'Commence'
        self._initialize_connection()
        try:
            conversation_obj = self.commence_app.GetConversation(application_name, topic)
            if conversation_obj is None:
                raise ValueError(f'Could not create conversation object for {application_name}!{topic}')
            return ConversationAPI(conversation_obj)
        except Exception as e:
            raise

        # com_inited = False
        # try:
        #     try:
        #         pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        #         com_inited = True
        #     except pythoncom.com_error:
        #         pass
        #     return self.establish_conversation_raw(*args, **kwargs)
        #
        # finally:
        #     if com_inited:
        #         pythoncom.CoUninitialize()

    def establish_conversation_raw(
            self, topic: DDETopic, application_name: _t.Literal['Commence'] = 'Commence'
    ) -> ConversationAPI:
        conversation_obj = self.commence_app.GetConversation(application_name, topic)
        if conversation_obj is None:
            raise ValueError(f'Could not create conversation object for {application_name}!{topic}')
        return ConversationAPI(conversation_obj)

    @property
    def name(self) -> str:
        """(read-only) Name of the Commence database."""
        if self._name is None:
            self._name = self.commence_app.Name
        return self._name

    @property
    def path(self) -> str:
        """(read-only) Full path of the Commence database."""
        if self._path is None:
            self._path = self.commence_app.Path
        return self._path

    @property
    def registered_user(self) -> str:
        """(read-only) CR/LF delimited string with username, company name, and serial number."""
        if self._registered_user is None:
            self._registered_user = self.commence_app.RegisteredUser
        return self._registered_user

    @property
    def shared(self) -> bool:
        """(read-only) TRUE if the database is enrolled in a workgroup."""
        if self._shared is None:
            self._shared = self.commence_app.Shared
        return self._shared

    @property
    def version(self) -> str:
        """(read-only) Version number in x.y format."""
        if self._version is None:
            self._version = self.commence_app.Version
        return self._version

    @property
    def version_ext(self) -> str:
        """(read-only) Version number in x.y.z.w format."""
        if self._version_ext is None:
            self._version_ext = self.commence_app.VersionExt
        return self._version_ext

    def __str__(self) -> str:
        return f'<Cmc: "{self.name}">'

    def __repr__(self):
        name = self._name if self._name is not None else '<COM?>'
        return f'<Cmc: {name}>'
