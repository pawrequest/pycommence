from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pythoncom
import win32com.client
from win32.lib.pywintypes import IID
from win32com.client import Dispatch, DispatchBaseClass
from win32com.universal import com_error

from pycommence.icommence.const import LCID, CursorType, OptionFlag

if TYPE_CHECKING:
    from pycommence.icommence.conversation import ICommenceConversation
    from pycommence.icommence.cursor import ICommenceCursor


class ICommenceDB(DispatchBaseClass):
    CLSID = IID('{92A04260-BE5C-11D1-99CC-00C04FD3695E}')
    coclass_clsid = IID('{92A04261-BE5C-11D1-99CC-00C04FD3695E}')

    def GetConversation(self, application_name, topic) -> ICommenceConversation:
        try:
            ret = self._oleobj_.InvokeTypes(40, LCID, 1, (9, 0), ((8, 1), (8, 1)), application_name, topic)
            if ret is not None:
                ret = Dispatch(ret, 'GetConversation', '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}')
            return cast(ICommenceConversation, cast(object, ret))
        except com_error as e:
            raise RuntimeError(f'Failed to get conversation for {application_name}!{topic}') from e

    def GetCursor(self, mode: CursorType, name: str, flags: OptionFlag = OptionFlag.NONE) -> ICommenceCursor:
        try:
            ret = self._oleobj_.InvokeTypes(20, 0, 1, (9, 0), ((3, 1), (8, 1), (3, 1)), mode, name, flags)
            if ret is not None:
                ret = Dispatch(ret, 'ICommenceCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
            return cast(ICommenceCursor, cast(object, ret))
        except com_error as e:
            raise RuntimeError('Failed to get cursor') from e

    def MLValidate(self, pszRequiredVersion):
        return self._oleobj_.InvokeTypes(50, LCID, 1, (3, 0), ((8, 1),), pszRequiredVersion)

    _prop_map_get_ = {
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'Path': (2, 2, (8, 0), (), 'Path', None),
        'RegisteredUser': (6, 2, (8, 0), (), 'RegisteredUser', None),
        'Shared': (3, 2, (11, 0), (), 'Shared', None),
        'Version': (4, 2, (8, 0), (), 'Version', None),
        'VersionExt': (5, 2, (8, 0), (), 'VersionExt', None),
    }
    _prop_map_put_ = {
        'Name': ((1, LCID, 4, 0), ()),
        'Path': ((2, LCID, 4, 0), ()),
        'RegisteredUser': ((6, LCID, 4, 0), ()),
        'Shared': ((3, LCID, 4, 0), ()),
        'Version': ((4, LCID, 4, 0), ()),
        'VersionExt': ((5, LCID, 4, 0), ()),
    }

    def __iter__(self):
        """Return a Python iterator for this object"""
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return win32com.client.util.Iterator(ob, None)
