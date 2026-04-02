import pythoncom
from win32.lib.pywintypes import IID
from win32com import client

# from win32com.client import DispatchBaseClass

DispatchBaseClass = client.CDispatch
from pycommence.icommence.const import LCID


class ICommenceConversation(DispatchBaseClass):
    CLSID = IID('{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}')
    coclass_clsid = None

    def Execute(self, pszCommand):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((8, 1),), pszCommand)

    def Request(self, pszCommand):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((8, 1),), pszCommand)

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)
