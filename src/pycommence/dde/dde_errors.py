from __future__ import annotations

from functools import wraps
from collections.abc import Callable

import dde
import pythoncom
import pywintypes

from pycommence.core.exceptions import PyCommenceError


def dde_error_code_lookup(code: int) -> str:
    if 0 < code < 100:
        return f'Invalid Data at position {code}'
    return DDEErrorDict.get(code, 'Unknown DDE error code.')


def commence_pycom_error_code(e: pywintypes.com_error) -> int:
    long_code, basic_msg, code_tup, sometype = e.args
    code = code_tup[0]
    return int(code)


class PyCmcDDEError(PyCommenceError):
    def __init__(self, cmd: str, code: int, msg: str | None = None, og_exception: Exception | None = None):
        self.cmd = cmd
        self.code = code
        self.dde_msg = dde_error_code_lookup(code)
        self.msg = msg if msg is not None else self.dde_msg
        super().__init__(self.msg)

    def __str__(self):
        return f'DDE Error {self.code} for command "{self.cmd}": {self.msg} ({self.dde_msg})'


class PyCmcDDENoConnectionError(PyCmcDDEError):
    def __init__(self):
        super().__init__(cmd='N/A', code=600, msg='DDE connection failed.')


def raise_for_bad_dde(cmd: str, res):
    if isinstance(res, str) and res == '(Active item not found)':
        raise PyCmcDDEError(cmd=cmd, code=610)


def dde_handler(func: Callable):
    """ Decorator to handle lock and DDE errors for DDEServer methods. First Arg must be DDEServer instance. """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # if not isinstance(args[0], DDEServer):
        #     raise ValueError('DDE Error handler - requires DDEServer as first argument')
        self = args[0]
        cmd = str(args[1]) if len(args) > 1 else func.__name__
        try:
            res = func(*args, **kwargs)
            raise_for_bad_dde(cmd, res)
            return res

        except pythoncom.error as e:
            long_code, basic_msg, code_tup, sometype, rest = e.args
            code = code_tup[0]
            raise PyCmcDDEError(cmd, code) from e

        except dde.error as e:
            try:
                code = self._last_error_no_handler()
                raise PyCmcDDEError(cmd, code) from e
            except Exception as e2:
                if isinstance(e2, dde.error):
                    e.add_note('Additionally, failed to get DDE error code from server.')
                    raise e
                raise e2 from e

    return wrapper


DDEErrorDict = {
    100: 'Out of memory',
    101: 'Internal error',
    102: ' Wrong number of parameters',
    103: 'Unknown conversation topic',
    104: 'No Phone Log category has been set, returned by LogPhoneCall EXECUTE command. Use Customize-Preferences-Event Logs to select a category.',
    105: 'No category selected; returned by ViewData REQUESTS not preceded by a ViewCategory.',
    106: 'Unsupported clipboard format',
    107: 'Unsupported field type',
    108: 'Field/qualifier mismatch; returned by ViewFilter REQUEST',
    109: 'Unknown EXECUTE command',
    110: 'Parsing error. Check syntax of DDE command.',
    111: 'Unknown REQUEST item or parsing error',
    112: 'Cannot add new item, category full; returned by AddItem, AddSharedItem and LogPhoneCall EXECUTE commands.',
    113: 'File I/O error. Is the disk full?',
    114: 'Connection already exists; returned by the AssignConnection EXECUTE command',
    115: 'No such connection exists; returned by the UnassignConnection EXECUTE commands',
    116: 'The category has been invalidated',
    117: 'The item has been invalidated.',
    118: 'An "every" date was received, or is the default value for a date field. Date ranges are not supported via DDE; returned by the AddItem or EditItem EXECUTE commands',
    119: 'Non-unique item name; returned by the AddItem or EditItem EXECUTE commands',
    120: 'Parameter too long; returned by the AddItem, EditItem and AppendText EXECUTE commands',
    121: 'No active child window or child window is unsupported; returned by the GetActiveViewInfo and GetLetterViewInfo REQUESTS',
    122: 'Agents are currently disabled. Returned by FireTrigger.',
    123: 'No item has been marked. Use ViewMarkItem or AddItem to mark an item.',
    124: 'Incompatible image type. Returned by GetImageFieldToFile or ViewImageFieldToFile.',
    125: 'Permission denied. Workgroup client does not have correct permission level.',
    126: 'No (-Me-) item has been defined. Use Customize-Preferences-Personal Info.',
    127: 'TAPI error encountered.',
    128: 'An agent exists but it is currently inactive. Returned by FireTrigger.',
    201: 'Filter 1 has been invalidated; this may occur if a ToCategory item is deleted/modified',
    202: 'Filter 2 has been invalidated',
    203: 'Filter 3 has been invalidated',
    204: 'Filter 4 has been invalidated',
    600: 'Cannot Connect to server application',
    610: 'PyCmc: Active Item not found',
}
