# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.12.0 (tags/v3.12.0:0fb18b0, Oct  2 2023, 13:03:39) [MSC v.1935 64 bit (AMD64)]
# From type library 'US_FORM.TLB'
# On Wed Oct 11 22:12:08 2023
'Commence RM Type Library'
makepy_version = '0.5.01'
python_version = 0x30c00f0

import pythoncom
import win32com.client.CLSIDToClass
import win32com.client.util
from win32.lib.pywintypes import IID
from win32com.client import Dispatch

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg = pythoncom.Empty
defaultNamedNotOptArg = pythoncom.Empty
defaultUnnamedArg = pythoncom.Empty

CLSID = IID('{C92C33EC-2A72-11D0-8A93-444553540000}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 8
LCID = 0x0

from win32com.client import DispatchBaseClass


class IApp(DispatchBaseClass):
    'IApp Interface'
    CLSID = IID('{9419F0A3-A8ED-11D4-824C-0050DAC366C6}')
    coclass_clsid = IID('{9419F0A4-A8ED-11D4-824C-0050DAC366C6}')

    def GetCursor(self, nMode=defaultNamedNotOptArg, nFlag=defaultNamedNotOptArg):
        'method GetCursor'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), ((3, 0), (3, 0)), nMode
                                         , nFlag)

    def Version(self):
        'method Version'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(1, LCID, 1, (8, 0), (), )

    def quit(self):
        'method quit'
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), (), )

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICmcApplication(DispatchBaseClass):
    CLSID = IID('{18884001-732C-11D0-AC0A-00A02485EC15}')
    coclass_clsid = None

    def IsScriptLevelSupported(self, level=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), ((3, 1),), level
                                         )

    _prop_map_get_ = {
        "CurrentScriptLevel": (7, 2, (3, 0), (), "CurrentScriptLevel", None),
        "Database": (9, 2, (9, 0), (), "Database", None),
        "DatabaseDirectory": (5, 2, (8, 0), (), "DatabaseDirectory", None),
        "DatabaseName": (4, 2, (8, 0), (), "DatabaseName", None),
        "DefaultScriptLevel": (6, 2, (3, 0), (), "DefaultScriptLevel", None),
        "Name": (1, 2, (8, 0), (), "Name", None),
        "ProgramDirectory": (3, 2, (8, 0), (), "ProgramDirectory", None),
        "ProgramName": (2, 2, (8, 0), (), "ProgramName", None),
        "Version": (8, 2, (8, 0), (), "Version", None),
    }
    _prop_map_put_ = {
        "CurrentScriptLevel": ((7, LCID, 4, 0), ()),
        "Database": ((9, LCID, 4, 0), ()),
        "DatabaseDirectory": ((5, LCID, 4, 0), ()),
        "DatabaseName": ((4, LCID, 4, 0), ()),
        "DefaultScriptLevel": ((6, LCID, 4, 0), ()),
        "Name": ((1, LCID, 4, 0), ()),
        "ProgramDirectory": ((3, LCID, 4, 0), ()),
        "ProgramName": ((2, LCID, 4, 0), ()),
        "Version": ((8, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceAddRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags
                                         )

    # Result is of type ICommenceCursor
    def CommitGetCursor(self, flags=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(25, LCID, 1, (9, 0), ((3, 1),), flags
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'CommitGetCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetColumnIndex(self, pLabel=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel
                                         , flags)

    def GetColumnLabel(self, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol
                                         , flags)

    def GetRow(self, nRow=defaultNamedNotOptArg, pDelim=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(26, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow
                                         , pDelim, flags)

    def GetRowValue(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow
                                         , nCol, flags)

    def GetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    def ModifyRow(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, pBuf=defaultNamedNotOptArg,
                  flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1), (3, 1)), nRow
                                         , nCol, pBuf, flags)

    def SetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    _prop_map_get_ = {
        "ColumnCount": (2, 2, (3, 0), (), "ColumnCount", None),
        "RowCount": (1, 2, (3, 0), (), "RowCount", None),
    }
    _prop_map_put_ = {
        "ColumnCount": ((2, LCID, 4, 0), ()),
        "RowCount": ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceConversation(DispatchBaseClass):
    CLSID = IID('{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}')
    coclass_clsid = None

    def Execute(self, pszCommand=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((8, 1),), pszCommand
                                         )

    def Request(self, pszCommand=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((8, 1),), pszCommand
                                         )

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceCursor(DispatchBaseClass):
    CLSID = IID('{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    # Result is of type ICommenceAddRowSet
    def GetAddRowSet(self, nCount=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceAddRowSet':
        ret = self._oleobj_.InvokeTypes(28, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetAddRowSet', '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceDeleteRowSet
    def GetDeleteRowSet(self, nCount=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceDeleteRowSet':
        ret = self._oleobj_.InvokeTypes(31, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetDeleteRowSet', '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceDeleteRowSet
    def GetDeleteRowSetByID(self, pRowID=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceDeleteRowSet':
        ret = self._oleobj_.InvokeTypes(32, LCID, 1, (9, 0), ((8, 1), (3, 1)), pRowID
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetDeleteRowSetByID', '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceEditRowSet
    def GetEditRowSet(self, nCount=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceEditRowSet':
        ret = self._oleobj_.InvokeTypes(29, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetEditRowSet', '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceEditRowSet
    def GetEditRowSetByID(self, pRowID=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceEditRowSet':
        ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((8, 1), (3, 1)), pRowID
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetEditRowSetByID', '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceQueryRowSet
    def GetQueryRowSet(self, nCount=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceQueryRowSet':
        ret = self._oleobj_.InvokeTypes(26, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetQueryRowSet', '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceQueryRowSet
    def GetQueryRowSetByID(self, pRowID=defaultNamedNotOptArg, flags=defaultNamedNotOptArg) -> 'ICommenceQueryRowSet':
        ret = self._oleobj_.InvokeTypes(27, LCID, 1, (9, 0), ((8, 1), (3, 1)), pRowID
                                        , flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetQueryRowSetByID', '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def SeekRow(self, bkOrigin=defaultNamedNotOptArg, nRows=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1), (3, 1)), bkOrigin
                                         , nRows)

    def SeekRowApprox(self, nNumerator=defaultNamedNotOptArg, nDenom=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (3, 0), ((3, 1), (3, 1)), nNumerator
                                         , nDenom)

    def SetActiveDate(self, sDate=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(34, LCID, 1, (11, 0), ((8, 1), (3, 1)), sDate
                                         , flags)

    def SetActiveDateRange(self, startDate=defaultNamedNotOptArg, endDate=defaultNamedNotOptArg,
                           flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(35, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), startDate
                                         , endDate, flags)

    def SetActiveItem(self, pCategoryName=defaultNamedNotOptArg, pRowID=defaultNamedNotOptArg,
                      flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(33, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), pCategoryName
                                         , pRowID, flags)

    def SetColumn(self, nColumn=defaultNamedNotOptArg, pName=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (11, 0), ((3, 1), (8, 1), (3, 1)), nColumn
                                         , pName, flags)

    def SetFilter(self, pFilter=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), ((8, 1), (3, 1)), pFilter
                                         , flags)

    def SetLogic(self, pLogic=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((8, 1), (3, 1)), pLogic
                                         , flags)

    def SetRelatedColumn(self, nColumn=defaultNamedNotOptArg, pConnName=defaultNamedNotOptArg,
                         pCatName=defaultNamedNotOptArg, pName=defaultNamedNotOptArg
                         , flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(36, LCID, 1, (11, 0), ((3, 1), (8, 1), (8, 1), (8, 1), (3, 1)), nColumn
                                         , pConnName, pCatName, pName, flags)

    def SetSort(self, pSort=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((8, 1), (3, 1)), pSort
                                         , flags)

    _prop_map_get_ = {
        "Category": (1, 2, (8, 0), (), "Category", None),
        "ColumnCount": (3, 2, (3, 0), (), "ColumnCount", None),
        "MaxFieldSize": (5, 2, (3, 0), (), "MaxFieldSize", None),
        "MaxRows": (6, 2, (3, 0), (), "MaxRows", None),
        "RowCount": (2, 2, (3, 0), (), "RowCount", None),
        "Shared": (4, 2, (11, 0), (), "Shared", None),
    }
    _prop_map_put_ = {
        "Category": ((1, LCID, 4, 0), ()),
        "ColumnCount": ((3, LCID, 4, 0), ()),
        "MaxFieldSize": ((5, LCID, 4, 0), ()),
        "MaxRows": ((6, LCID, 4, 0), ()),
        "RowCount": ((2, LCID, 4, 0), ()),
        "Shared": ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceDB(DispatchBaseClass):
    CLSID = IID('{92A04260-BE5C-11D1-99CC-00C04FD3695E}')
    coclass_clsid = IID('{92A04261-BE5C-11D1-99CC-00C04FD3695E}')

    # Result is of type ICommenceConversation
    def GetConversation(self, pszApplicationName=defaultNamedNotOptArg,
                        pszTopic=defaultNamedNotOptArg) -> ICommenceConversation:
        ret = self._oleobj_.InvokeTypes(40, LCID, 1, (9, 0), ((8, 1), (8, 1)), pszApplicationName
                                        , pszTopic)
        if ret is not None:
            ret = Dispatch(ret, 'GetConversation', '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}')
        return ret

    # Result is of type ICommenceCursor
    def GetCursor(self, nMode=defaultNamedNotOptArg, pName=defaultNamedNotOptArg,
                  flags=defaultNamedNotOptArg) -> 'ICommenceCursor':
        ret = self._oleobj_.InvokeTypes(20, LCID, 1, (9, 0), ((3, 1), (8, 1), (3, 1)), nMode
                                        , pName, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def MLValidate(self, pszRequiredVersion=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(50, LCID, 1, (3, 0), ((8, 1),), pszRequiredVersion
                                         )

    _prop_map_get_ = {
        "Name": (1, 2, (8, 0), (), "Name", None),
        "Path": (2, 2, (8, 0), (), "Path", None),
        "RegisteredUser": (6, 2, (8, 0), (), "RegisteredUser", None),
        "Shared": (3, 2, (11, 0), (), "Shared", None),
        "Version": (4, 2, (8, 0), (), "Version", None),
        "VersionExt": (5, 2, (8, 0), (), "VersionExt", None),
    }
    _prop_map_put_ = {
        "Name": ((1, LCID, 4, 0), ()),
        "Path": ((2, LCID, 4, 0), ()),
        "RegisteredUser": ((6, LCID, 4, 0), ()),
        "Shared": ((3, LCID, 4, 0), ()),
        "Version": ((4, LCID, 4, 0), ()),
        "VersionExt": ((5, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceDeleteRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags
                                         )

    def DeleteRow(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetColumnIndex(self, pLabel=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel
                                         , flags)

    def GetColumnLabel(self, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol
                                         , flags)

    def GetRow(self, nRow=defaultNamedNotOptArg, pDelim=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(25, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow
                                         , pDelim, flags)

    def GetRowID(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(27, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowTimeStamp(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(28, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowValue(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow
                                         , nCol, flags)

    def GetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(26, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    _prop_map_get_ = {
        "ColumnCount": (2, 2, (3, 0), (), "ColumnCount", None),
        "RowCount": (1, 2, (3, 0), (), "RowCount", None),
    }
    _prop_map_put_ = {
        "ColumnCount": ((2, LCID, 4, 0), ()),
        "RowCount": ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceEditRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags
                                         )

    # Result is of type ICommenceCursor
    def CommitGetCursor(self, flags=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(25, LCID, 1, (9, 0), ((3, 1),), flags
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'CommitGetCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetColumnIndex(self, pLabel=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel
                                         , flags)

    def GetColumnLabel(self, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol
                                         , flags)

    def GetRow(self, nRow=defaultNamedNotOptArg, pDelim=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(26, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow
                                         , pDelim, flags)

    def GetRowID(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(29, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowTimeStamp(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(30, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowValue(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow
                                         , nCol, flags)

    def GetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    def ModifyRow(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, pBuf=defaultNamedNotOptArg,
                  flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1), (3, 1)), nRow
                                         , nCol, pBuf, flags)

    def SetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    _prop_map_get_ = {
        "ColumnCount": (2, 2, (3, 0), (), "ColumnCount", None),
        "RowCount": (1, 2, (3, 0), (), "RowCount", None),
    }
    _prop_map_put_ = {
        "ColumnCount": ((2, LCID, 4, 0), ()),
        "RowCount": ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ICommenceQueryRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def GetColumnIndex(self, pLabel=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel
                                         , flags)

    def GetColumnLabel(self, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol
                                         , flags)

    def GetFieldToFile(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, filename=defaultNamedNotOptArg,
                       flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(26, LCID, 1, (3, 0), ((3, 1), (3, 1), (8, 1), (3, 1)), nRow
                                         , nCol, filename, flags)

    def GetRow(self, nRow=defaultNamedNotOptArg, pDelim=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(23, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow
                                         , pDelim, flags)

    def GetRowID(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(24, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowTimeStamp(self, nRow=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(27, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow
                                         , flags)

    def GetRowValue(self, nRow=defaultNamedNotOptArg, nCol=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow
                                         , nCol, flags)

    def GetShared(self, nRow=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (11, 0), ((3, 1),), nRow
                                         )

    _prop_map_get_ = {
        "ColumnCount": (2, 2, (3, 0), (), "ColumnCount", None),
        "RowCount": (1, 2, (3, 0), (), "RowCount", None),
    }
    _prop_map_put_ = {
        "ColumnCount": ((2, LCID, 4, 0), ()),
        "RowCount": ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IConnOA(DispatchBaseClass):
    CLSID = IID('{47A27291-7572-11D0-AC0B-00A02485EC15}')
    coclass_clsid = None

    def Clear(self):
        return self._oleobj_.InvokeTypes(10, LCID, 1, (11, 0), (), )

    def ClearAll(self):
        return self._oleobj_.InvokeTypes(11, LCID, 1, (11, 0), (), )

    def ClearConnection(self, ItemName=defaultNamedNotOptArg, Clarify=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(12, LCID, 1, (11, 0), ((8, 1), (8, 1)), ItemName
                                         , Clarify)

    def FieldValue(self, FieldName=defaultNamedNotOptArg):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(14, LCID, 1, (8, 0), ((8, 1),), FieldName
                                         )

    def RestoreFilter(self):
        return self._oleobj_.InvokeTypes(18, LCID, 1, (11, 0), (), )

    def SetActiveDate(self, sDate=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(16, LCID, 1, (11, 0), ((8, 1), (3, 1)), sDate
                                         , flags)

    def SetActiveDateRange(self, startDate=defaultNamedNotOptArg, endDate=defaultNamedNotOptArg,
                           flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(17, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), startDate
                                         , endDate, flags)

    def SetActiveItem(self, pCategoryName=defaultNamedNotOptArg, ItemName=defaultNamedNotOptArg,
                      Clarify=defaultNamedNotOptArg, flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(15, LCID, 1, (11, 0), ((8, 1), (8, 1), (8, 1), (3, 1)), pCategoryName
                                         , ItemName, Clarify, flags)

    def SetConnection(self, ItemName=defaultNamedNotOptArg, Clarify=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(13, LCID, 1, (11, 0), ((8, 1), (8, 1)), ItemName
                                         , Clarify)

    def SetFilterKeyword(self, sKeyword=defaultNamedNotOptArg, sValue=defaultNamedNotOptArg,
                         flags=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(19, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), sKeyword
                                         , sValue, flags)

    _prop_map_get_ = {
        "ConnectedItemCount": (3, 2, (3, 0), (), "ConnectedItemCount", None),
        "CurrentSelection": (5, 2, (3, 0), (), "CurrentSelection", None),
        "ItemClarifyField": (7, 2, (8, 0), (), "ItemClarifyField", None),
        "ItemName": (6, 2, (8, 0), (), "ItemName", None),
        "Name": (1, 2, (8, 0), (), "Name", None),
        "ToCategory": (2, 2, (8, 0), (), "ToCategory", None),
        "UnconnectedItemCount": (4, 2, (3, 0), (), "UnconnectedItemCount", None),
    }
    _prop_map_put_ = {
        "ConnectedItemCount": ((3, LCID, 4, 0), ()),
        "CurrentSelection": ((5, LCID, 4, 0), ()),
        "ItemClarifyField": ((7, LCID, 4, 0), ()),
        "ItemName": ((6, LCID, 4, 0), ()),
        "Name": ((1, LCID, 4, 0), ()),
        "ToCategory": ((2, LCID, 4, 0), ()),
        "UnconnectedItemCount": ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IControlOA(DispatchBaseClass):
    CLSID = IID('{F180CB64-D4F0-464B-8EB6-0008689A24A6}')
    coclass_clsid = None

    def ActiveXGetProperty(self, PropertyName=defaultNamedNotOptArg, Parameter1=defaultNamedNotOptArg):
        return self._ApplyTypes_(2, 1, (12, 0), ((8, 1), (12, 1)), 'ActiveXGetProperty', None, PropertyName
                                 , Parameter1)

    def ActiveXMethod(self, MethodName=defaultNamedNotOptArg, ParameterArr=defaultNamedNotOptArg):
        return self._ApplyTypes_(4, 1, (12, 0), ((8, 1), (8204, 3)), 'ActiveXMethod', None, MethodName
                                 , ParameterArr)

    def ActiveXSetProperty(self, PropertyName=defaultNamedNotOptArg, Parameter1=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(3, LCID, 1, (11, 0), ((8, 1), (16396, 1)), PropertyName
                                         , Parameter1)

    _prop_map_get_ = {
        "ControlName": (1, 2, (8, 0), (), "ControlName", None),
    }
    _prop_map_put_ = {
        "ControlName": ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IDatabaseOA(DispatchBaseClass):
    CLSID = IID('{845A7A11-88F6-11D0-AC0E-00A02485EC15}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Name": (1, 2, (8, 0), (), "Name", None),
        "Path": (2, 2, (8, 0), (), "Path", None),
        "Version": (3, 2, (8, 0), (), "Version", None),
    }
    _prop_map_put_ = {
        "Name": ((1, LCID, 4, 0), ()),
        "Path": ((2, LCID, 4, 0), ()),
        "Version": ((3, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IFieldOA(DispatchBaseClass):
    CLSID = IID('{383CFA14-73D5-11D0-AC0B-00A02485EC15}')
    coclass_clsid = None

    _prop_map_get_ = {
        "Label": (2, 2, (8, 0), (), "Label", None),
        "Name": (1, 2, (8, 0), (), "Name", None),
        "Value": (3, 2, (8, 0), (), "Value", None),
    }
    _prop_map_put_ = {
        "Label": ((2, LCID, 4, 0), ()),
        "Name": ((1, LCID, 4, 0), ()),
        "Value": ((3, LCID, 4, 0), ()),
    }

    # Default property for this class is 'Value'
    def __call__(self):
        return self._ApplyTypes_(*(3, 2, (8, 0), (), "Value", None))

    def __str__(self, *args):
        return str(self.__call__(*args))

    def __int__(self, *args):
        return int(self.__call__(*args))

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IFormOA(DispatchBaseClass):
    CLSID = IID('{654E7740-2AB6-11D0-8A93-444553540000}')
    coclass_clsid = IID('{654E7741-2AB6-11D0-8A93-444553540000}')

    def Abort(self):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (11, 0), (), )

    def Cancel(self):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (11, 0), (), )

    # Result is of type IConnOA
    def Connection(self, ConnectionName=defaultNamedNotOptArg, CategoryName=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((8, 1), (8, 1)), ConnectionName
                                        , CategoryName)
        if ret is not None:
            ret = Dispatch(ret, 'Connection', '{47A27291-7572-11D0-AC0B-00A02485EC15}')
        return ret

    # Result is of type IControlOA
    def Control(self, ControlName=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(31, LCID, 1, (9, 0), ((8, 1),), ControlName
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'Control', '{F180CB64-D4F0-464B-8EB6-0008689A24A6}')
        return ret

    # Result is of type IFieldOA
    def Field(self, FieldName=defaultNamedNotOptArg):
        ret = self._oleobj_.InvokeTypes(29, LCID, 1, (9, 0), ((8, 1),), FieldName
                                        )
        if ret is not None:
            ret = Dispatch(ret, 'Field', '{383CFA14-73D5-11D0-AC0B-00A02485EC15}')
        return ret

    def MoveToField(self, FieldName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (24, 0), ((8, 1),), FieldName
                                         )

    def MoveToTab(self, TabName=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (24, 0), ((8, 1),), TabName
                                         )

    def Save(self):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (11, 0), (), )

    def SetShared(self, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((3, 1),), Value
                                         )

    def SetValue(self, Value=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((8, 1),), Value
                                         )

    _prop_map_get_ = {
        # Property 'Application' is an object of type 'ICmcApplication'
        "Application": (6, 2, (9, 0), (), "Application", '{18884001-732C-11D0-AC0A-00A02485EC15}'),
        "BackColor": (11, 2, (19, 0), (), "BackColor", None),
        "Caption": (12, 2, (8, 0), (), "Caption", None),
        "CategoryName": (2, 2, (8, 0), (), "CategoryName", None),
        "FieldName": (5, 2, (8, 0), (), "FieldName", None),
        "FieldValue": (8, 2, (8, 0), (), "FieldValue", None),
        "IsAdd": (7, 2, (11, 0), (), "IsAdd", None),
        "IsShared": (9, 2, (11, 0), (), "IsShared", None),
        "ItemName": (3, 2, (8, 0), (), "ItemName", None),
        "Name": (1, 2, (8, 0), (), "Name", None),
        "Runtime": (10, 2, (9, 0), (), "Runtime", None),
        "TabName": (4, 2, (8, 0), (), "TabName", None),
    }
    _prop_map_put_ = {
        "Application": ((6, LCID, 4, 0), ()),
        "BackColor": ((11, LCID, 4, 0), ()),
        "Caption": ((12, LCID, 4, 0), ()),
        "CategoryName": ((2, LCID, 4, 0), ()),
        "FieldName": ((5, LCID, 4, 0), ()),
        "FieldValue": ((8, LCID, 4, 0), ()),
        "IsAdd": ((7, LCID, 4, 0), ()),
        "IsShared": ((9, LCID, 4, 0), ()),
        "ItemName": ((3, LCID, 4, 0), ()),
        "Name": ((1, LCID, 4, 0), ()),
        "Runtime": ((10, LCID, 4, 0), ()),
        "TabName": ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IFullControl(DispatchBaseClass):
    'IFullControl Interface'
    CLSID = IID('{BE0B47E8-0BD2-4114-923E-EEFFEB740942}')
    coclass_clsid = IID('{789D254B-2D9B-487C-BABF-89D0EF6BD76C}')

    def myfunction(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
        'method myfunction'
        return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), ((3, 1), (3, 1)), x
                                         , y)

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class ISimple(DispatchBaseClass):
    'ISimple Interface'
    CLSID = IID('{1C9DF726-86D4-4C5B-8398-7418F0903597}')
    coclass_clsid = IID('{DADC9CCF-FA28-4738-B142-B4CBD17267A6}')

    def MyEventCallback(self, id=defaultNamedNotOptArg, pVarResult=defaultNamedNotOptArg):
        'method MyEventCallback'
        return self._oleobj_.InvokeTypes(3, LCID, 1, (24, 0), ((3, 0), (16396, 0)), id
                                         , pVarResult)

    def Test(self):
        'method Test'
        return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (), )

    def Version(self):
        'method Version'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(2, LCID, 1, (8, 0), (), )

    _prop_map_get_ = {
        "Application": (5, 2, (9, 0), (), "Application", None),
        "Database": (4, 2, (9, 0), (), "Database", None),
    }
    _prop_map_put_ = {
        "Application": ((5, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class IUIObj(DispatchBaseClass):
    'IUIObj Interface'
    CLSID = IID('{2BAE3CB5-A80C-11D4-A632-0040D0051497}')
    coclass_clsid = IID('{2BAE3CB6-A80C-11D4-A632-0040D0051497}')

    def Application(self):
        'method Application'
        ret = self._oleobj_.InvokeTypes(3, LCID, 1, (9, 0), (), )
        if ret is not None:
            ret = Dispatch(ret, 'Application', None)
        return ret

    def GetTest(self, bstrVal=defaultNamedNotOptArg):
        'method GetTest'
        return self._oleobj_.InvokeTypes(5, LCID, 1, (24, 0), ((16392, 0),), bstrVal
                                         )

    def GoToURL(self):
        'method GoToURL'
        return self._oleobj_.InvokeTypes(2, LCID, 1, (24, 0), (), )

    def HelloHTML(self):
        'method HelloHTML'
        return self._oleobj_.InvokeTypes(1, LCID, 1, (24, 0), (), )

    def OnClick(self, pdispBody=defaultNamedNotOptArg, varColor=defaultNamedNotOptArg):
        return self._oleobj_.InvokeTypes(1610743808, LCID, 1, (24, 0), ((9, 1), (12, 1)), pdispBody
                                         , varColor)

    def Test(self):
        'method Test'
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(4, LCID, 1, (8, 0), (), )

    def clickIn(self, x=defaultNamedNotOptArg, y=defaultNamedNotOptArg):
        'method clickIn'
        return self._oleobj_.InvokeTypes(6, LCID, 1, (24, 0), ((3, 1), (3, 1)), x
                                         , y)

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class Isample(DispatchBaseClass):
    'Isample Interface'
    CLSID = IID('{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}')
    coclass_clsid = IID('{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}')

    _prop_map_get_ = {
    }
    _prop_map_put_ = {
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError("This object does not support enumeration")
        return win32com.client.util.Iterator(ob, None)


class _DFormOAEvents:
    'Event interface for FormOA object'
    CLSID = CLSID_Sink = IID('{654E7742-2AB6-11D0-8A93-444553540000}')
    coclass_clsid = IID('{654E7741-2AB6-11D0-8A93-444553540000}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
        1: "OnLoad",
        2: "OnSave",
        3: "OnCancel",
        4: "OnEnterTab",
        5: "OnLeaveTab",
        6: "OnEnterField",
        7: "OnLeaveField",
        8: "OnEnterControl",
        9: "OnLeaveControl",
        10: "OnClick",
        11: "OnChange",
        12: "OnKeyPress",
        13: "OnActiveXControlEvent",
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
            cp, cookie, self._olecp, self._olecp_cookie = self._olecp, self._olecp_cookie, None, None
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util
        if iid == self.CLSID_Sink: return win32com.server.util.wrap(self)

# Event Handlers
# If you create handlers, they should have the following prototypes:


#	def OnLoad(self):
#	def OnSave(self):
#	def OnCancel(self):
#	def OnEnterTab(self, Tab=defaultNamedNotOptArg):
#	def OnLeaveTab(self, Tab=defaultNamedNotOptArg):
#	def OnEnterField(self, Field=defaultNamedNotOptArg):
#	def OnLeaveField(self, Field=defaultNamedNotOptArg):
#	def OnEnterControl(self, ControlID=defaultNamedNotOptArg):
#	def OnLeaveControl(self, ControlID=defaultNamedNotOptArg):
#	def OnClick(self, ControlID=defaultNamedNotOptArg):
#	def OnChange(self, ControlID=defaultNamedNotOptArg):
#	def OnKeyPress(self, ControlID=defaultNamedNotOptArg, KeyAscii=defaultNamedNotOptArg):
#	def OnActiveXControlEvent(self, ControlName=defaultNamedNotOptArg, EventName=defaultNamedNotOptArg, ParameterArr=defaultNamedNotOptArg):


class _IFullControlEvents:
    '_IFullControlEvents Interface'
    CLSID = CLSID_Sink = IID('{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}')
    coclass_clsid = IID('{789D254B-2D9B-487C-BABF-89D0EF6BD76C}')
    _public_methods_ = []  # For COM Server support
    _dispid_to_func_ = {
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
            cp, cookie, self._olecp, self._olecp_cookie = self._olecp, self._olecp_cookie, None, None
            cp.Unadvise(cookie)

    def _query_interface_(self, iid):
        import win32com.server.util
        if iid == self.CLSID_Sink: return win32com.server.util.wrap(self)

# Event Handlers
# If you create handlers, they should have the following prototypes:


from win32com.client import CoClassBaseClass


class App(CoClassBaseClass):  # A CoClass
    # App Class
    CLSID = IID('{9419F0A4-A8ED-11D4-824C-0050DAC366C6}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IApp,
    ]
    default_interface = IApp


# This CoClass is known by the name 'Commence.DB'
class CommenceDB(CoClassBaseClass):  # A CoClass
    CLSID = IID('{92A04261-BE5C-11D1-99CC-00C04FD3695E}')
    coclass_sources = [
    ]
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
    coclass_sources = [
    ]
    coclass_interfaces = [
        ISimple,
    ]
    default_interface = ISimple


class UIObj(CoClassBaseClass):  # A CoClass
    # UIObj Class
    CLSID = IID('{2BAE3CB6-A80C-11D4-A632-0040D0051497}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        IUIObj,
    ]
    default_interface = IUIObj


class sample(CoClassBaseClass):  # A CoClass
    # sample Class
    CLSID = IID('{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}')
    coclass_sources = [
    ]
    coclass_interfaces = [
        Isample,
    ]
    default_interface = Isample


IApp_vtables_dispatch_ = 1
IApp_vtables_ = [
    (('Version', 'bstrVersion',), 1, (1, (), [(16392, 10, None, None), ], 1, 1, 4, 0, 56, (3, 0, None, None), 0,)),
    (('GetCursor', 'nMode', 'nFlag', 'pName',), 2, (2, (), [
        (3, 0, None, None), (3, 0, None, None), (16392, 10, None, None), ], 1, 1, 4, 0, 64, (3, 0, None, None), 0,)),
    (('quit',), 3, (3, (), [], 1, 1, 4, 0, 72, (3, 0, None, None), 0,)),
]

IFullControl_vtables_dispatch_ = 1
IFullControl_vtables_ = [
    (('myfunction', 'x', 'y',), 1, (1, (), [(3, 1, None, None),
                                            (3, 1, None, None), ], 1, 1, 4, 0, 56, (3, 0, None, None), 0,)),
]

ISimple_vtables_dispatch_ = 1
ISimple_vtables_ = [
    (('Test',), 1, (1, (), [], 1, 1, 4, 0, 56, (3, 0, None, None), 0,)),
    (('Version', 'bstrVersion',), 2, (2, (), [(16392, 10, None, None), ], 1, 1, 4, 0, 64, (3, 0, None, None), 0,)),
    (('MyEventCallback', 'id', 'pVarResult',), 3, (3, (), [(3, 0, None, None),
                                                           (16396, 0, None, None), ], 1, 1, 4, 0, 72,
                                                   (3, 0, None, None), 0,)),
    (('Database', 'pVal',), 4, (4, (), [(16393, 10, None, None), ], 1, 2, 4, 0, 80, (3, 0, None, None), 0,)),
    (('Application', 'pVal',), 5, (5, (), [(16393, 10, None, None), ], 1, 2, 4, 0, 88, (3, 0, None, None), 0,)),
    (('Application', 'pVal',), 5, (5, (), [(9, 1, None, None), ], 1, 4, 4, 0, 96, (3, 0, None, None), 0,)),
]

IUIObj_vtables_dispatch_ = 1
IUIObj_vtables_ = [
    (('OnClick', 'pdispBody', 'varColor',), 1610743808, (1610743808, (), [(9, 1, None, None),
                                                                          (12, 1, None, None), ], 1, 1, 4, 0, 56,
                                                         (3, 0, None, None), 0,)),
    (('HelloHTML',), 1, (1, (), [], 1, 1, 4, 0, 64, (3, 0, None, None), 0,)),
    (('GoToURL',), 2, (2, (), [], 1, 1, 4, 0, 72, (3, 0, None, None), 0,)),
    (('Application', 'pApp',), 3, (3, (), [(16393, 10, None, None), ], 1, 1, 4, 0, 80, (3, 0, None, None), 0,)),
    (('Test', 'bstrVal',), 4, (4, (), [(16392, 10, None, None), ], 1, 1, 4, 0, 88, (3, 0, None, None), 0,)),
    (('GetTest', 'bstrVal',), 5, (5, (), [(16392, 0, None, None), ], 1, 1, 4, 0, 96, (3, 0, None, None), 0,)),
    (('clickIn', 'x', 'y',), 6, (6, (), [(3, 1, None, None),
                                         (3, 1, None, None), ], 1, 1, 4, 0, 104, (3, 0, None, None), 0,)),
]

Isample_vtables_dispatch_ = 1
Isample_vtables_ = [
]

RecordMap = {
}

CLSIDToClassMap = {
    '{18884001-732C-11D0-AC0A-00A02485EC15}': ICmcApplication,
    '{383CFA14-73D5-11D0-AC0B-00A02485EC15}': IFieldOA,
    '{F180CB64-D4F0-464B-8EB6-0008689A24A6}': IControlOA,
    '{47A27291-7572-11D0-AC0B-00A02485EC15}': IConnOA,
    '{845A7A11-88F6-11D0-AC0E-00A02485EC15}': IDatabaseOA,
    '{654E7740-2AB6-11D0-8A93-444553540000}': IFormOA,
    '{654E7742-2AB6-11D0-8A93-444553540000}': _DFormOAEvents,
    '{654E7741-2AB6-11D0-8A93-444553540000}': FormOA,
    '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}': ICommenceCursor,
    '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}': ICommenceQueryRowSet,
    '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}': ICommenceAddRowSet,
    '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}': ICommenceEditRowSet,
    '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}': ICommenceDeleteRowSet,
    '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}': ICommenceConversation,
    '{92A04260-BE5C-11D1-99CC-00C04FD3695E}': ICommenceDB,
    '{92A04261-BE5C-11D1-99CC-00C04FD3695E}': CommenceDB,
    '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}': Isample,
    '{F22497D6-AAC1-4DA4-9DC7-CD5C1536431C}': sample,
    '{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}': _IFullControlEvents,
    '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}': IFullControl,
    '{789D254B-2D9B-487C-BABF-89D0EF6BD76C}': FullControl,
    '{1C9DF726-86D4-4C5B-8398-7418F0903597}': ISimple,
    '{DADC9CCF-FA28-4738-B142-B4CBD17267A6}': Simple,
    '{2BAE3CB5-A80C-11D4-A632-0040D0051497}': IUIObj,
    '{2BAE3CB6-A80C-11D4-A632-0040D0051497}': UIObj,
    '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}': IApp,
    '{9419F0A4-A8ED-11D4-824C-0050DAC366C6}': App,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict(CLSIDToClassMap)
VTablesToPackageMap = {}
VTablesToClassMap = {
    '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}': 'Isample',
    '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}': 'IFullControl',
    '{1C9DF726-86D4-4C5B-8398-7418F0903597}': 'ISimple',
    '{2BAE3CB5-A80C-11D4-A632-0040D0051497}': 'IUIObj',
    '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}': 'IApp',
}

NamesToIIDMap = {
    'ICmcApplication': '{18884001-732C-11D0-AC0A-00A02485EC15}',
    'IFieldOA': '{383CFA14-73D5-11D0-AC0B-00A02485EC15}',
    'IControlOA': '{F180CB64-D4F0-464B-8EB6-0008689A24A6}',
    'IConnOA': '{47A27291-7572-11D0-AC0B-00A02485EC15}',
    'IDatabaseOA': '{845A7A11-88F6-11D0-AC0E-00A02485EC15}',
    'IFormOA': '{654E7740-2AB6-11D0-8A93-444553540000}',
    '_DFormOAEvents': '{654E7742-2AB6-11D0-8A93-444553540000}',
    'ICommenceCursor': '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceQueryRowSet': '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceAddRowSet': '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceEditRowSet': '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceDeleteRowSet': '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}',
    'ICommenceConversation': '{9D1EB82D-6F4F-4DCF-BF8C-9E0D33FE83E1}',
    'ICommenceDB': '{92A04260-BE5C-11D1-99CC-00C04FD3695E}',
    'Isample': '{6F0D28AA-9A6E-44B2-AAF5-A98FFD14B2C1}',
    '_IFullControlEvents': '{8C5813AA-6C64-4B5F-BC50-BD2C768CD066}',
    'IFullControl': '{BE0B47E8-0BD2-4114-923E-EEFFEB740942}',
    'ISimple': '{1C9DF726-86D4-4C5B-8398-7418F0903597}',
    'IUIObj': '{2BAE3CB5-A80C-11D4-A632-0040D0051497}',
    'IApp': '{9419F0A3-A8ED-11D4-824C-0050DAC366C6}',
}
