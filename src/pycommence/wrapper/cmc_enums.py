from enum import Enum


class CursorType(Enum):
    """ note missing 4 as per original cmc spec
        types 7+ appear in docs->Constants->GetCursor but not in GetCursor method spec
                """
    # open based on a category, columns = all supported fields in the category (in no particular order).
    CATEGORY = 0

    # Valid view-types: report, grid, report viewer, and book/address book.
    # inherit the view's filter, sort, and column set.
    # ICommenceCursor methods can be used to change these attributes.
    VIEW = 1

    # All Pilot* cursor column-sets =  defined by the Commence preferences (in no particular order).
    # It is not possible to change the filter, sort, or column set.

    # Category and fields defined by Preferences-> Other Apps -> 3Com Pilot Address Book.
    PILOT_ADDRESS = 2

    # Category and fields defined by Preferences-> Other Apps -> 3Com Pilot Memo Pad.
    PILOT_MEMO = 3

    # Category and fields defined by Preferences -> Other Apps -> 3Com Pilot To Do List.
    PILOT_TODO = 5

    # Category and fields defined by Preferences -> Other Apps -> 3Com Pilot Date Book.
    PILOT_APPOINT = 6

    # MS Outlook contacts preference
    OUTLOOK_ADDRESS = 7

    # MS Outlook calendar preference
    OUTLOOK_APPOINT = 8

    # MS Outlook Email Log preference
    OUTLOOK_EMAIL_LOG = 9

    # MS Outlook Task preference
    OUTLOOK_TASK = 10

    # open based on the view data used with the Send Letter command
    LETTER_MERGE = 11


class Bookmark(Enum):
    BEGINNING = 0
    CURRENT = 1
    END = 2


class OptionFlag(Enum):
    NONE = 0
    FIELD_NAME = 0x0001
    ALL = 0x0002
    SHARED = 0x0004
    PILOT = 0x0008
    CANONICAL = 0x0010
    INTERNET = 0x0020


FLAGS_UNUSED = 0


