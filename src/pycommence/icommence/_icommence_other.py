from typing import TYPE_CHECKING

from pycommence.icommence.const import LCID, OptionFlag
from pycommence.icommence.db import ICommenceDB

if TYPE_CHECKING:
    pass

import pythoncom
from win32.lib.pywintypes import IID
from win32com import client
from win32com.client import Dispatch, DispatchBaseClass


class IApp(DispatchBaseClass):
    """IApp Interface"""

    CLSID = IID('{9419F0A3-A8ED-11D4-824C-0050DAC366C6}')
    coclass_clsid = IID('{9419F0A4-A8ED-11D4-824C-0050DAC366C6}')

    def GetCursor(self, mode: int, flags: int = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), ((3, 0), (3, 0)), mode, flags)

    def Version(self):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), ())

    def quit(self):
        """method quit"""
        return self._oleobj_.InvokeTypes(
            3,
            LCID,
            1,
            (24, 0),
            (),
        )

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class ICmcApplication(DispatchBaseClass):
    CLSID = IID('{18884001-732C-11D0-AC0A-00A02485EC15}')
    coclass_clsid = None

    def IsScriptLevelSupported(self, level):
        return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), ((3, 1),), level)

    _prop_map_get_ = {
        'CurrentScriptLevel': (7, 2, (3, 0), (), 'CurrentScriptLevel', None),
        'Database': (9, 2, (9, 0), (), 'Database', None),
        'DatabaseDirectory': (5, 2, (8, 0), (), 'DatabaseDirectory', None),
        'DatabaseName': (4, 2, (8, 0), (), 'DatabaseName', None),
        'DefaultScriptLevel': (6, 2, (3, 0), (), 'DefaultScriptLevel', None),
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'ProgramDirectory': (3, 2, (8, 0), (), 'ProgramDirectory', None),
        'ProgramName': (2, 2, (8, 0), (), 'ProgramName', None),
        'Version': (8, 2, (8, 0), (), 'Version', None),
    }
    _prop_map_put_ = {
        'CurrentScriptLevel': ((7, LCID, 4, 0), ()),
        'Database': ((9, LCID, 4, 0), ()),
        'DatabaseDirectory': ((5, LCID, 4, 0), ()),
        'DatabaseName': ((4, LCID, 4, 0), ()),
        'DefaultScriptLevel': ((6, LCID, 4, 0), ()),
        'Name': ((1, LCID, 4, 0), ()),
        'ProgramDirectory': ((3, LCID, 4, 0), ()),
        'ProgramName': ((2, LCID, 4, 0), ()),
        'Version': ((8, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IConnOA(DispatchBaseClass):
    CLSID = IID('{47A27291-7572-11D0-AC0B-00A02485EC15}')
    coclass_clsid = None

    def Clear(self):
        return self._oleobj_.InvokeTypes(
            10,
            LCID,
            1,
            (11, 0),
            (),
        )

    def ClearAll(self):
        return self._oleobj_.InvokeTypes(
            11,
            LCID,
            1,
            (11, 0),
            (),
        )

    def ClearConnection(self, ItemName, Clarify):
        return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), ((8, 1), (8, 1)), ItemName, Clarify)

    def FieldValue(self, FieldName):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(14, LCID, 1, (8, 0), ((8, 1),), FieldName)

    def RestoreFilter(self):
        return self._oleobj_.InvokeTypes(
            18,
            LCID,
            1,
            (11, 0),
            (),
        )

    def SetActiveDate(self, sDate, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(16, LCID, 1, (11, 0), ((8, 1), (3, 1)), sDate, flags)

    def SetActiveDateRange(
        self,
        startDate,
        endDate,
        flags,
    ):
        return self._oleobj_.InvokeTypes(17, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), startDate, endDate, flags)

    def SetActiveItem(
        self,
        pCategoryName,
        ItemName,
        Clarify,
        flags,
    ):
        return self._oleobj_.InvokeTypes(
            15,
            LCID,
            1,
            (11, 0),
            ((8, 1), (8, 1), (8, 1), (3, 1)),
            pCategoryName,
            ItemName,
            Clarify,
            flags,
        )

    def SetConnection(self, ItemName, Clarify):
        return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), ((8, 1), (8, 1)), ItemName, Clarify)

    def SetFilterKeyword(
        self,
        sKeyword,
        sValue,
        flags,
    ):
        return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), sKeyword, sValue, flags)

    _prop_map_get_ = {
        'ConnectedItemCount': (3, 2, (3, 0), (), 'ConnectedItemCount', None),
        'CurrentSelection': (5, 2, (3, 0), (), 'CurrentSelection', None),
        'ItemClarifyField': (7, 2, (8, 0), (), 'ItemClarifyField', None),
        'ItemName': (6, 2, (8, 0), (), 'ItemName', None),
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'ToCategory': (2, 2, (8, 0), (), 'ToCategory', None),
        'UnconnectedItemCount': (4, 2, (3, 0), (), 'UnconnectedItemCount', None),
    }
    _prop_map_put_ = {
        'ConnectedItemCount': ((3, LCID, 4, 0), ()),
        'CurrentSelection': ((5, LCID, 4, 0), ()),
        'ItemClarifyField': ((7, LCID, 4, 0), ()),
        'ItemName': ((6, LCID, 4, 0), ()),
        'Name': ((1, LCID, 4, 0), ()),
        'ToCategory': ((2, LCID, 4, 0), ()),
        'UnconnectedItemCount': ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IControlOA(DispatchBaseClass):
    CLSID = IID('{F180CB64-D4F0-464B-8EB6-0008689A24A6}')
    coclass_clsid = None

    def ActiveXGetProperty(self, PropertyName, Parameter1):
        return self._ApplyTypes_(
            2,
            1,
            (12, 0),
            ((8, 1), (12, 1)),
            'ActiveXGetProperty',
            None,
            PropertyName,
            Parameter1,
        )

    def ActiveXMethod(self, MethodName, ParameterArr):
        return self._ApplyTypes_(
            4,
            1,
            (12, 0),
            ((8, 1), (8204, 3)),
            'ActiveXMethod',
            None,
            MethodName,
            ParameterArr,
        )

    def ActiveXSetProperty(self, PropertyName, Parameter1):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((8, 1), (16396, 1)), PropertyName, Parameter1)

    _prop_map_get_ = {
        'ControlName': (1, 2, (8, 0), (), 'ControlName', None),
    }
    _prop_map_put_ = {
        'ControlName': ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IDatabaseOA(DispatchBaseClass):
    CLSID = IID('{845A7A11-88F6-11D0-AC0E-00A02485EC15}')
    coclass_clsid = None

    _prop_map_get_ = {
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'Path': (2, 2, (8, 0), (), 'Path', None),
        'Version': (3, 2, (8, 0), (), 'Version', None),
    }
    _prop_map_put_ = {
        'Name': ((1, LCID, 4, 0), ()),
        'Path': ((2, LCID, 4, 0), ()),
        'Version': ((3, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IFieldOA(DispatchBaseClass):
    CLSID = IID('{383CFA14-73D5-11D0-AC0B-00A02485EC15}')
    coclass_clsid = None

    _prop_map_get_ = {
        'Label': (2, 2, (8, 0), (), 'Label', None),
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'Value': (3, 2, (8, 0), (), 'Value', None),
    }
    _prop_map_put_ = {
        'Label': ((2, LCID, 4, 0), ()),
        'Name': ((1, LCID, 4, 0), ()),
        'Value': ((3, LCID, 4, 0), ()),
    }

    # Default property for this class is 'Value'
    def __call__(self):
        return self._ApplyTypes_(*(3, 2, (8, 0), (), 'Value', None))

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IFormOA(DispatchBaseClass):
    CLSID = IID('{654E7740-2AB6-11D0-8A93-444553540000}')
    coclass_clsid = IID('{654E7741-2AB6-11D0-8A93-444553540000}')

    def Abort(self):
        return self._oleobj_.InvokeTypes(
            25,
            LCID,
            1,
            (11, 0),
            (),
        )

    def Cancel(self):
        return self._oleobj_.InvokeTypes(
            24,
            LCID,
            1,
            (11, 0),
            (),
        )

    # Result is of type IConnOA
    def Connection(self, ConnectionName, CategoryName):
        ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((8, 1), (8, 1)), ConnectionName, CategoryName)
        if ret is not None:
            ret = Dispatch(ret, 'Connection', '{47A27291-7572-11D0-AC0B-00A02485EC15}')
        return ret

    # Result is of type IControlOA
    def Control(self, ControlName):
        ret = self._oleobj_.InvokeTypes(31, LCID, 1, (9, 0), ((8, 1),), ControlName)
        if ret is not None:
            ret = Dispatch(ret, 'Control', '{F180CB64-D4F0-464B-8EB6-0008689A24A6}')
        return ret

    # Result is of type IFieldOA
    def Field(self, FieldName):
        ret = self._oleobj_.InvokeTypes(29, LCID, 1, (9, 0), ((8, 1),), FieldName)
        if ret is not None:
            ret = Dispatch(ret, 'Field', '{383CFA14-73D5-11D0-AC0B-00A02485EC15}')
        return ret

    def MoveToField(self, FieldName):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), ((8, 1),), FieldName)

    def MoveToTab(self, TabName):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((8, 1),), TabName)

    def Save(self):
        return self._oleobj_.InvokeTypes(
            23,
            LCID,
            1,
            (11, 0),
            (),
        )

    def SetShared(self, Value):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((3, 1),), Value)

    def SetValue(self, Value):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((8, 1),), Value)

    _prop_map_get_ = {
        # Property 'Application' is an object of type 'ICmcApplication'
        'Application': (
            6,
            2,
            (9, 0),
            (),
            'Application',
            '{18884001-732C-11D0-AC0A-00A02485EC15}',
        ),
        'BackColor': (11, 2, (19, 0), (), 'BackColor', None),
        'Caption': (12, 2, (8, 0), (), 'Caption', None),
        'CategoryName': (2, 2, (8, 0), (), 'CategoryName', None),
        'FieldName': (5, 2, (8, 0), (), 'FieldName', None),
        'FieldValue': (8, 2, (8, 0), (), 'FieldValue', None),
        'IsAdd': (7, 2, (11, 0), (), 'IsAdd', None),
        'IsShared': (9, 2, (11, 0), (), 'IsShared', None),
        'ItemName': (3, 2, (8, 0), (), 'ItemName', None),
        'Name': (1, 2, (8, 0), (), 'Name', None),
        'Runtime': (10, 2, (9, 0), (), 'Runtime', None),
        'TabName': (4, 2, (8, 0), (), 'TabName', None),
    }
    _prop_map_put_ = {
        'Application': ((6, LCID, 4, 0), ()),
        'BackColor': ((11, LCID, 4, 0), ()),
        'Caption': ((12, LCID, 4, 0), ()),
        'CategoryName': ((2, LCID, 4, 0), ()),
        'FieldName': ((5, LCID, 4, 0), ()),
        'FieldValue': ((8, LCID, 4, 0), ()),
        'IsAdd': ((7, LCID, 4, 0), ()),
        'IsShared': ((9, LCID, 4, 0), ()),
        'ItemName': ((3, LCID, 4, 0), ()),
        'Name': ((1, LCID, 4, 0), ()),
        'Runtime': ((10, LCID, 4, 0), ()),
        'TabName': ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IFullControl(DispatchBaseClass):
    "IFullControl Interface"

    CLSID = IID('{BE0B47E8-0BD2-4114-923E-EEFFEB740942}')
    coclass_clsid = IID('{789D254B-2D9B-487C-BABF-89D0EF6BD76C}')

    def myfunction(self, x, y):
        "method myfunction"
        return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((3, 1), (3, 1)), x, y)

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class ISimple(DispatchBaseClass):
    "ISimple Interface"

    CLSID = IID('{1C9DF726-86D4-4C5B-8398-7418F0903597}')
    coclass_clsid = IID('{DADC9CCF-FA28-4738-B142-B4CBD17267A6}')

    def MyEventCallback(self, id, pVarResult):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((3, 0), (16396, 0)), id, pVarResult)

    def Test(self):
        return self._oleobj_.InvokeTypes(
            1,
            LCID,
            1,
            (24, 0),
            (),
        )

    def Version(self):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(
            2,
            LCID,
            1,
            (8, 0),
            (),
        )

    _prop_map_get_ = {
        'Application': (5, 2, (9, 0), (), 'Application', None),
        'Database': (4, 2, (9, 0), (), 'Database', None),
    }
    _prop_map_put_ = {
        'Application': ((5, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class IUIObj(DispatchBaseClass):
    "IUIObj Interface"

    CLSID = IID('{2BAE3CB5-A80C-11D4-A632-0040D0051497}')
    coclass_clsid = IID('{2BAE3CB6-A80C-11D4-A632-0040D0051497}')

    def Application(self):
        ret = self._oleobj_.InvokeTypes(
            3,
            LCID,
            1,
            (9, 0),
            (),
        )
        if ret is not None:
            ret = Dispatch(ret, 'Application', None)
        return ret

    def GetTest(self, bstrVal):
        return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((16392, 0),), bstrVal)

    def GoToURL(self):
        return self._oleobj_.InvokeTypes(
            2,
            LCID,
            1,
            (24, 0),
            (),
        )

    def HelloHTML(self):
        return self._oleobj_.InvokeTypes(
            1,
            LCID,
            1,
            (24, 0),
            (),
        )

    def OnClick(self, pdispBody, varColor):
        return self._oleobj_.InvokeTypes(1610743808, LCID, 1, (24, 0), ((9, 1), (12, 1)), pdispBody, varColor)

    def Test(self):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(
            4,
            LCID,
            1,
            (8, 0),
            (),
        )

    def clickIn(self, x, y):
        return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((3, 1), (3, 1)), x, y)

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class Isample(DispatchBaseClass):
    CLSID = IID('{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}')
    coclass_clsid = IID('{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}')

    _prop_map_get_ = {}
    _prop_map_put_ = {}

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)


class _DFormOAEvents:
    "Event interface for FormOA object"

    CLSID = CLSID_Sink = IID('{654E7742-2AB6-11D0-8A93-444553540000}')
    coclass_clsid = IID('{654E7741-2AB6-11D0-8A93-444553540000}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
        1: 'OnLoad',
        2: 'OnSave',
        3: 'OnCancel',
        4: 'OnEnterTab',
        5: 'OnLeaveTab',
        6: 'OnEnterField',
        7: 'OnLeaveField',
        8: 'OnEnterControl',
        9: 'OnLeaveControl',
        10: 'OnClick',
        11: 'OnChange',
        12: 'OnKeyPress',
        13: 'OnActiveXControlEvent',
    }

    def __init__(self, oobj=None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy

            cpc = oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp = cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie = cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp, self._olecp_cookie = cp, cookie

    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass

    def close(self):
        if self._olecp is not None:
            cp, cookie, self._olecp, self._olecp_cookie = (
                self._olecp,
                self._olecp_cookie,
                None,
                None,
            )
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util

        if iid == self.CLSID_Sink:
            return win32com.server.util.wrap(self)


# Event Handlers
# If you create handlers, they should have the following prototypes:


# def OnLoad(self):
# def OnSave(self):
# def OnCancel(self):
# def OnEnterTab(self, Tab):
# def OnLeaveTab(self, Tab):
# def OnEnterField(self, Field):
# def OnLeaveField(self, Field):
# def OnEnterControl(self, ControlID):
# def OnLeaveControl(self, ControlID):
# def OnClick(self, ControlID):
# def OnChange(self, ControlID):
# def OnKeyPress(self, ControlID, KeyAscii):
# def OnActiveXControlEvent(self, ControlName, EventName, ParameterArr):


class _IFullControlEvents:
    CLSID = CLSID_Sink = IID('{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}')
    coclass_clsid = IID('{789D254B-2D9B-487C-BABF-89D0EF6BD76C}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {}

    def __init__(self, oobj=None):
        if oobj is None:
            self._olecp = None
        else:
            import win32com.server.util
            from win32com.server.policy import EventHandlerPolicy

            cpc = oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
            cp = cpc.FindConnectionPoint(self.CLSID_Sink)
            cookie = cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
            self._olecp, self._olecp_cookie = cp, cookie

    def __del__(self):
        try:
            self.close()
        except pythoncom.com_error:
            pass

    def close(self):
        if self._olecp is not None:
            cp, cookie, self._olecp, self._olecp_cookie = (
                self._olecp,
                self._olecp_cookie,
                None,
                None,
            )
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util

        if iid == self.CLSID_Sink:
            return win32com.server.util.wrap(self)


# Event Handlers
# If you create handlers, they should have the following prototypes:


from win32com.client import CoClassBaseClass


class App(CoClassBaseClass):  # A CoClass
    # App Class
    CLSID = IID('{9419F0A4-A8ED-11D4-824C-0050DAC366C6}')
    coclass_sources = []
    coclass_interfaces = [
        IApp,
    ]
    default_interface = IApp


# This CoClass is known by the name 'Commence.DB'
class CommenceDB(CoClassBaseClass):  # A CoClass
    CLSID = IID('{92A04261-BE5C-11D1-99CC-00C04FD3695E}')
    coclass_sources = []
    coclass_interfaces = [
        ICommenceDB,
    ]
    default_interface = ICommenceDB


class FormOA(CoClassBaseClass):  # A CoClass
    CLSID = IID('{654E7741-2AB6-11D0-8A93-444553540000}')
    coclass_sources = [
        _DFormOAEvents,
    ]
    default_source = _DFormOAEvents
    coclass_interfaces = [
        IFormOA,
    ]
    default_interface = IFormOA


class FullControl(CoClassBaseClass):  # A CoClass
    # FullControl Class
    CLSID = IID('{789D254B-2D9B-487C-BABF-89D0EF6BD76C}')
    coclass_sources = [
        _IFullControlEvents,
    ]
    default_source = _IFullControlEvents
    coclass_interfaces = [
        IFullControl,
    ]
    default_interface = IFullControl


class Simple(CoClassBaseClass):  # A CoClass
    # Simple Class
    CLSID = IID('{DADC9CCF-FA28-4738-B142-B4CBD17267A6}')
    coclass_sources = []
    coclass_interfaces = [
        ISimple,
    ]
    default_interface = ISimple


class UIObj(CoClassBaseClass):  # A CoClass
    # UIObj Class
    CLSID = IID('{2BAE3CB6-A80C-11D4-A632-0040D0051497}')
    coclass_sources = []
    coclass_interfaces = [
        IUIObj,
    ]
    default_interface = IUIObj


class sample(CoClassBaseClass):  # A CoClass
    # sample Class
    CLSID = IID('{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}')
    coclass_sources = []
    coclass_interfaces = [
        Isample,
    ]
    default_interface = Isample
