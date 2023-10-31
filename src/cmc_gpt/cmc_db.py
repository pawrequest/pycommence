from win32com.client import Dispatch

from cmc_gpt.cmc_cursor import CommenceCursor
from cmc_gpt.cmc_conversation import CommenceConversation


class CmcDB:
    def __init__(self):
        self.cmc_db = Dispatch("Commence.DB")

    @property
    def name(self) -> str:
        """(read-only) Name of the Commence database."""
        return self.cmc_db.Name

    @property
    def path(self) -> str:
        """(read-only) Full path of the Commence database."""
        return self.cmc_db.Path

    @property
    def registered_user(self) -> str:
        """(read-only) CR/LF delimited string with username, company name, and serial number."""
        return self.cmc_db.RegisteredUser

    @property
    def shared(self) -> bool:
        """(read-only) TRUE if the database is enrolled in a workgroup."""
        return self.cmc_db.Shared

    @property
    def version(self) -> str:
        """(read-only) Version number in x.y format."""
        return self.cmc_db.Version

    @property
    def version_ext(self) -> str:
        """(read-only) Version number in x.y.z.w format."""
        return self.cmc_db.VersionExt

    def get_conversation(self, topic: str, application_name: str = "Commence") -> CommenceConversation:
        """
        Create a conversation object, except probably just don't and go get a cursor instead.

        Args:
            application_name (str): DDE Application name. The only valid value is "Commence".
            topic (str): DDE Topic name, must be a valid Commence topic name.
                         Examples include "GetData", "ViewData", etc.

        Returns:
            CommenceConversation: A CommenceConversation object on success, None on failure.
        """
        conversation_obj = self.cmc_db.GetConversation(application_name, topic)
        if conversation_obj is None:
            raise ValueError(f"Could not create conversation object for {application_name}!{topic}")
        return CommenceConversation(conversation_obj)

    def get_cursor(self) -> CommenceCursor:
        """
        Create a cursor object.

        Returns:
            CommenceCursor: A CommenceCursor object.
        """
        return CommenceCursor(self.cmc_db.GetCursor())
