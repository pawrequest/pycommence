"""
DDE ERROR CODES
105 (0x69) No category selected; returned by ViewData REQUESTS not preceded by a ViewCategory.

106 (0x6A) Unsupported clipboard format

107 (0x6B) Unsupported field type

108 (0x6C) Field/qualifier mismatch; returned by ViewFilter REQUEST

109 (0x6D) Unknown EXECUTE command

110 (0x6E) Parsing error. Check syntax of DDE command.

111 (0x6F) Unknown REQUEST item or parsing error

112 (0x70) Cannot add new item, category full; returned by AddItem, AddSharedItem and LogPhoneCall EXECUTE commands.

113 (0x71) File I/O error. Is the disk full?

114 (0x72) Connection already exists; returned by the AssignConnection EXECUTE command

115 (0x73) No such connection exists; returned by the UnassignConnection EXECUTE commands

116 (0x74) The category has been invalidated

117 (0x75) The item has been invalidated.

118 (0x76) An "every" date was received, or is the default value for a date field. Date ranges are not supported via DDE; returned by the AddItem or EditItem EXECUTE commands

119 (0x77) Non-unique item name; returned by the AddItem or EditItem EXECUTE commands

120 (0x78) Parameter too long; returned by the AddItem, EditItem and AppendText EXECUTE commands

121 (0x79) No active child window or child window is unsupported; returned by the GetActiveViewInfo and GetLetterViewInfo REQUESTS

122 (0x80) Agents are currently disabled. Returned by FireTrigger.

123 (0x81) No item has been marked. Use ViewMarkItem or AddItem to mark an item.

124 (0x82) Incompatible image type. Returned by GetImageFieldToFile or ViewImageFieldToFile.

125 (0x83) Permission denied. Workgroup client does not have correct permission level.

126 (0x84) No (-Me-) item has been defined. Use Customize-Preferences-Personal Info.

127 (0x85) TAPI error encountered.

128 (0x86) An agent exists but it is currently inactive. Returned by FireTrigger.

201 (0xC9) Filter 1 has been invalidated; this may occur if a ToCategory item is deleted/modified

202 (0xCA) Filter 2 has been invalidated

203 (0xCB) Filter 3 has been invalidated

204 (0xCC) Filter 4 has been invalidated

"""

from __future__ import annotations

from enum import StrEnum
from typing import Protocol

DDEErrorDict = {
    105: 'No category selected; returned by ViewData REQUESTS not preceded by a ViewCategory.',
    106: 'Unsupported clipboard format', 107: 'Unsupported field type',
    108: 'Field/qualifier mismatch; returned by ViewFilter REQUEST', 109: 'Unknown EXECUTE command',
    110: 'Parsing error. Check syntax of DDE command.', 111: 'Unknown REQUEST item or parsing error',
    112: 'Cannot add new item, category full; returned by AddItem, AddSharedItem and LogPhoneCall EXECUTE commands.',
    113: 'File I/O error. Is the disk full?',
    114: 'Connection already exists; returned by the AssignConnection EXECUTE command',
    115: 'No such connection exists; returned by the UnassignConnection EXECUTE commands',
    116: 'The category has been invalidated', 117: 'The item has been invalidated.',
    118: 'An "every" date was received, or is the default value for a date field. Date ranges are not supported via DDE; returned by the AddItem or EditItem EXECUTE commands',
    119: 'Non-unique item name; returned by the AddItem or EditItem EXECUTE commands',
    120: 'Parameter too long; returned by the AddItem, EditItem and AppendText EXECUTE commands',
    121: 'No active child window or child window is unsupported; returned by the GetActiveViewInfo and GetLetterViewInfo REQUESTS',
    122: 'Agents are currently disabled. Returned by FireTrigger.',
    123: 'No item has been marked. Use ViewMarkItem or AddItem to mark an item.',
    124: 'Incompatible image type. Returned by GetImageFieldToFile or ViewImageFieldToFile.',
    125: 'Permission denied. Workgroup client does not have correct permission level.',
    126: 'No (-Me-) item has been defined. Use Customize-Preferences-Personal Info.', 127: 'TAPI error encountered.',
    128: 'An agent exists but it is currently inactive. Returned by FireTrigger.',
    201: 'Filter 1 has been invalidated; this may occur if a ToCategory item is deleted/modified',
    202: 'Filter 2 has been invalidated', 203: 'Filter 3 has been invalidated', 204: 'Filter 4 has been invalidated'
}


class CmcError(Exception):
    def __init__(self, msg: str = ''):
        self.msg = msg
        super().__init__(self.msg)


class PyCommenceError(Exception):
    pass


class PyCommenceExistsError(PyCommenceError):
    pass


class PyCommenceDDEError(PyCommenceError):
    def __init__(self, cmd:str, code: int, msg: str | None = None):
        self.code = code
        self.cmd = cmd
        self.msg = msg or DDEErrorDict.get(code, f'Unknown DDE error code: {code}')
        super().__init__(self.msg)

    def __str__(self):
        return f'DDE Error {self.code} for command "{self.cmd}": {self.msg}'


class PyCommenceNotFoundError(PyCommenceError):
    pass


class PyCommenceMaxExceededError(PyCommenceError):
    pass


class PyCommenceServerError(PyCommenceError):
    pass


class Handle(StrEnum):
    IGNORE = 'ignore'
    RAISE = 'raise'
    UPDATE = 'update'
    REPLACE = 'replace'
    ALL = 'all'


# def handle_existing(self, rs: HasRowCount, existing: HandleExisting, pk_val, tblname):
#     if rs.row_count > 0:
#         match existing:
#             case 'raise':
#                 raise PyCommenceExistsError()
#             case 'update':
#                 row_set = csr.get_edit_rowset()
#                 logger.debug(f'Updating record with primary key {pk_val}')
#             case 'replace':
#                 self.delete_record(pk_val=pk_val, csrname=tblname)
#                 row_set = csr.get_named_addset(pk_val)
#                 logger.debug(f'Replacing record with primary key {pk_val}')
#             case _:
#                 raise ValueError(f'Invalid value for existing: {existing}')
#         return row_set


class HasRowCount(Protocol):
    @property
    def row_count(self) -> int:
        ...


def raise_for_one(res: HasRowCount):
    if res.row_count == 0:
        raise PyCommenceNotFoundError('Row not found.')
    if res.row_count > 1:
        raise PyCommenceMaxExceededError('Multiple rows found')
