from win32com.client import Dispatch


class CommenceDB:
    def __init__(self, db_id):
        self.db_id = db_id
        self.cmc_db = Dispatch(f"Commence.DB.{db_id}")

    @property
    def name(self):
        return self.cmc_db.Name

    @property
    def path(self):
        return self.cmc_db.Path

    @property
    def registered_user(self):
        return self.cmc_db.RegisteredUser

    @property
    def shared(self):
        return self.cmc_db.Shared

    @property
    def version(self):
        return self.cmc_db.Version

    @property
    def version_ext(self):
        return self.cmc_db.VersionExt

    def get_conversation(self):
        return CommenceConversation(self.cmc_db.GetConversation())

    def get_cursor(self):
        return CommenceCursor(self.cmc_db.GetCursor())


