from win32com.client import Dispatch

from .cmc_conversation import CommenceConversation
from .cmc_cursor import CmcCursor


class CmcDB:
    def __init__(self):
        self._cmc = Dispatch('Commence.DB')

    @property
    def name(self) -> str:
        """(read-only) Name of the Commence database."""
        return self._cmc.Name

    @property
    def path(self) -> str:
        """(read-only) Full path of the Commence database."""
        return self._cmc.Path

    @property
    def registered_user(self) -> str:
        """(read-only) CR/LF delimited string with username, company name, and serial number."""
        return self._cmc.RegisteredUser

    @property
    def shared(self) -> bool:
        """(read-only) TRUE if the database is enrolled in a workgroup."""
        return self._cmc.Shared

    @property
    def version(self) -> str:
        """(read-only) Version number in x.y format."""
        return self._cmc.Version

    @property
    def version_ext(self) -> str:
        """(read-only) Version number in x.y.z.w format."""
        return self._cmc.VersionExt

    def get_conversation(
            self, topic: str, application_name: str = 'Commence'
    ) -> CommenceConversation:
        """
        Create a conversation object, except probably just don't and go get a cursor instead.

        Args:
            application_name (str): DDE Application name. The only valid value is "Commence".
            topic (str): DDE Topic name, must be a valid Commence topic name.
                         Examples include "GetData", "ViewData", etc.

        Returns:
            CommenceConversation: A CommenceConversation object on success, None on failure.
        """
        conversation_obj = self._cmc.GetConversation(application_name, topic)
        if conversation_obj is None:
            raise ValueError(
                f'Could not create conversation object for {application_name}!{topic}'
            )
        return CommenceConversation(conversation_obj)

    def get_cursor(self, name: str, mode: int = 0, flags: int = 0) -> CmcCursor:
        """
        Create a cursor object for accessing Commence data.

        Parameters:
        mode (int): Type of Commence data to access with this cursor. Valid values are:
            0 - CMC_CURSOR_CATEGORY: Use the Commence category specified by name.
            1 - CMC_CURSOR_VIEW: Use the Commence view specified by name.
            2 - CMC_CURSOR_PILOTAB: Use the Commence category and fields defined from
                 Preferences - Other Apps - 3Com Pilot Address Book.
            3 - CMC_CURSOR_PILOTMEMO: Use the Commence category and fields defined from
                 Preferences - Other Apps - 3Com Pilot Memo Pad.
            5 - CMC_CURSOR_PILOTTODO: Use the Commence category and fields defined from
                 Preferences - Other Apps - 3Com Pilot To Do List.
            6 - CMC_CURSOR_PILOTAPPT: Use the Commence category and fields defined from
                 Preferences - Other Apps - 3Com Pilot Date Book.
        name (str, optional): Name of an object in the database. Usage determined by mode.
            For CMC_CURSOR_CATEGORY, name is the category name.
            For CMC_CURSOR_VIEW, name is the view name.
            For CMC_CURSOR_PILOT*, name is unused. Defaults to ''.
        flags (int, optional): Additional option flags. Logical OR of the following option flags:
            CMC_FLAG_PILOT - Save Item agents defined for the Pilot subsystem will fire.
            CMC_FLAG_INTERNET - Save Item agents defined for the Internet/intranet will fire.
            Defaults to 0.

        Returns:
        CommenceCursor: A CommenceCursor object on success, None on failure.

        Comments:
        For CMC_CURSOR_CATEGORY, the resulting cursor will have a column set composed of all supported fields in the category (in no particular order).
        For CMC_CURSOR_VIEW, the resulting cursor will inherit the view's filter, sort, and column set. ICommenceCursor methods can be used to change these attributes.
        For CMC_CURSOR_PILOT*, the column set for the resulting cursor will only include fields defined by the Commence preferences (in no particular order). It is not possible to change the filter, sort, or column set.
        See the Developer Notes for more information about the CMC_FLAG_PILOT and CMC_FLAG_INTERNET flags.
        """
        return CmcCursor(self._cmc.GetCursor(mode, name, flags))
