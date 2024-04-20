from __future__ import annotations

import typing as _t

import win32com.client
from loguru import logger
from win32com.client import Dispatch
from win32com.universal import com_error

from pycommence import pycmc_types

from . import cmc_csr, conversation, enums_cmc


class CmcConnector:
    """Singleton managing cached connections to multiple Commence databases."""
    _connections: dict[str, Cmc] = {}

    def __new__(cls, commence_instance: str = 'Commence.DB') -> CmcConnector:
        if commence_instance in cls._connections:
            logger.info(f'Using cached connection to {commence_instance}')
        else:
            cls._connections[commence_instance] = super().__new__(Cmc)
            logger.info(f'Created new connection to {commence_instance}')

        return cls._connections[commence_instance]

    def __init__(self, db_name: str = 'Commence.DB'):
        self.db_name: str = db_name  # The name of the Commence instance.
        self._cmc_com: Dispatch = self._initialize_connection()  # The Commence COM object.
        self._initialized: bool = False  # True if the connection is established.

    def _initialize_connection(self) -> Dispatch:
        """Initialize the COM connection to the Commence database. """
        try:
            cmc_com: win32com.client.Dispatch = Dispatch(self.db_name)
            self._initialized = True
            return cmc_com
        except com_error as e:
            error_msg = f'Error connecting to {self.db_name}: {str(e)}'
            logger.error(error_msg)
            raise Exception(error_msg)

    # def __init__(self, commence_instance='Commence.DB'):
    #     if not hasattr(self, '_initialized'):
    #         self.db_name = commence_instance
    #         try:
    #             self._cmc_com: Dispatch = Dispatch(commence_instance)
    #             self._initialized = True
    #         except com_error as e:
    #             if e.hresult == -2147221005:
    #                 raise pycmc_types.CmcError(
    #                     f'Db Name "{commence_instance}" does not exist - connection failed'
    #                 )
    #             raise pycmc_types.CmcError(
    #                 f'Error connecting to {commence_instance}. Is Commence Running?\n{e}'
    #             )


class Cmc(CmcConnector):
    """ Commence Database object.

     Entry point for :class:`.cmc_csr.CsrCmc` and :class:`.conversation.CommenceConversation`.

     Caching Inherited from :class:`.CmcConnector`.

     Attributes:
        db_name (str): The name of the Commence instance.
        _cmc_com (Dispatch): The Commence COM object.
        _initialized (bool): True if the connection is established.

     """

    def get_cursor(
            self,
            name: str | None = None,
            mode: enums_cmc.CursorType = enums_cmc.CursorType.CATEGORY,
            flags: enums_cmc.OptionFlag | None = None
    ) -> cmc_csr.CsrCmc:
        """Create a cursor object for accessing Commence data.

        CursorTypes CATEGORY and VIEW require name to be set.

        Args:
            name (str|None): Name of the category or view to open.
            mode (enums_cmc.CursorType): Cursor type
            flags (enums_cmc.OptionFlag | None):
                - PILOT - Save Item agents defined for the Pilot subsystem will fire.
                - INTERNET - Save Item agents defined for the Internet/intranet will fire.

        Returns:
            CsrCmc: A Csr object on success.

        Raises:
            ValueError if no name given for name based searches

        """
        # todo can ther be multiple flags?
        if flags:
            if isinstance(flags, enums_cmc.OptionFlag):
                flags = [flags]
            for flag in flags:
                if flag not in [enums_cmc.OptionFlag.PILOT, enums_cmc.OptionFlag.INTERNET]:
                    raise ValueError(f'Invalid flag: {flag}')
            flags = ', '.join(str(f.value) for f in flags)

        else:
            flags = 0

        mode = mode.value
        if mode in [0, 1]:
            if name is None:
                raise ValueError(
                    f'Mode {mode} ("{enums_cmc.CursorType(mode).name}") requires name param to be set'
                )
        try:
            csr = cmc_csr.CsrCmc(self._cmc_com.GetCursor(mode, name, flags))
        except com_error as e:
            raise pycmc_types.CmcError(f'Error creating cursor for {name}: {e}')

        return csr
        # todo non-standard modes

    def get_conversation(
            self, topic: str, application_name: _t.Literal['Commence'] = 'Commence'
    ) -> conversation.CommenceConversation:
        """
        Create a conversation object.

        Args:
            topic (str): DDE Topic name, must be a valid Commence topic name.
            application_name (str): DDE Application name. The only valid value is "Commence".

        Returns:
            CommenceConversation: A CommenceConversation object on success.

        Raises:
            ValueError if failure.

        """

        conversation_obj = self._cmc_com.GetConversation(application_name, topic)
        if conversation_obj is None:
            raise ValueError(
                f'Could not create conversation object for {application_name}!{topic}'
            )
        return conversation.CommenceConversation(conversation_obj)

    @property
    def name(self) -> str:
        """(read-only) Name of the Commence database."""
        return self._cmc_com.Name

    @property
    def path(self) -> str:
        """(read-only) Full path of the Commence database."""
        return self._cmc_com.Path

    @property
    def registered_user(self) -> str:
        """(read-only) CR/LF delimited string with username, company name, and serial number."""
        return self._cmc_com.RegisteredUser

    @property
    def shared(self) -> bool:
        """(read-only) TRUE if the database is enrolled in a workgroup."""
        return self._cmc_com.Shared

    @property
    def version(self) -> str:
        """(read-only) Version number in x.y format."""
        return self._cmc_com.Version

    @property
    def version_ext(self) -> str:
        """(read-only) Version number in x.y.z.w format."""
        return self._cmc_com.VersionExt

    def __str__(self) -> str:
        return f'<Cmc: "{self.name}">'

    def __repr__(self):
        return f'<Cmc: {self.name}>'
