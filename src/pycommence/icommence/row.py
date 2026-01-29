from __future__ import annotations

import pythoncom
import win32com.client
from win32.lib.pywintypes import IID
from win32com.client import DispatchBaseClass, Dispatch

from pycommence.icommence.const import OptionFlag, LCID


class ICommenceAddRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags)

    # Result is of type ICommenceCursor
    def CommitGetCursor(self, flags: OptionFlag = OptionFlag.NONE):
        ret = self._oleobj_.InvokeTypes(25, LCID, 1, (9, 0), ((3, 1),), flags)
        if ret is not None:
            ret = Dispatch(ret, 'CommitGetCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetColumnIndex(self, column_name: str, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), column_name, flags)

    def GetColumnLabel(self, column_index: int, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), column_index, flags)

    def GetRow(self, nRow, pDelim, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(26, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow, pDelim, flags)

    def GetRowValue(self, nRow, nCol, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow, nCol, flags)

    def GetShared(self, nRow):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (11, 0), ((3, 1),), nRow)

    def ModifyRow(self, nRow, nCol, pBuf, flags, ):
        return self._oleobj_.InvokeTypes(
            23,
            LCID,
            1,
            (3, 0),
            ((3, 1), (3, 1), (8, 1), (3, 1)),
            nRow,
            nCol,
            pBuf,
            flags, )

    def SetShared(self, nRow):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (11, 0), ((3, 1),), nRow)

    _prop_map_get_ = {
        'ColumnCount': (2, 2, (3, 0), (), 'ColumnCount', None),
        'RowCount': (1, 2, (3, 0), (), 'RowCount', None),
    }
    _prop_map_put_ = {
        'ColumnCount': ((2, LCID, 4, 0), ()),
        'RowCount': ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        'Return a Python iterator for this object'
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return win32com.client.util.Iterator(ob, None)


class ICommenceDeleteRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags)

    def DeleteRow(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetColumnIndex(self, pLabel, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel, flags)

    def GetColumnLabel(self, nCol, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol, flags)

    def GetRow(self, nRow, pDelim, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(
            25, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow, pDelim, flags
        )

    def GetRowID(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(27, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowTimeStamp(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(28, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowValue(self, nRow, nCol, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow, nCol, flags)

    def GetShared(self, nRow):
        return self._oleobj_.InvokeTypes(26, LCID, 1, (11, 0), ((3, 1),), nRow)

    _prop_map_get_ = {
        'ColumnCount': (2, 2, (3, 0), (), 'ColumnCount', None),
        'RowCount': (1, 2, (3, 0), (), 'RowCount', None),
    }
    _prop_map_put_ = {
        'ColumnCount': ((2, LCID, 4, 0), ()),
        'RowCount': ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        'Return a Python iterator for this object'
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return win32com.client.util.Iterator(ob, None)


class ICommenceEditRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def Commit(self, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1),), flags)

    # Result is of type ICommenceCursor
    def CommitGetCursor(self, flags: OptionFlag = OptionFlag.NONE):
        ret = self._oleobj_.InvokeTypes(25, LCID, 1, (9, 0), ((3, 1),), flags)
        if ret is not None:
            ret = Dispatch(ret, 'CommitGetCursor', '{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetColumnIndex(self, pLabel, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel, flags)

    def GetColumnLabel(self, nCol, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol, flags)

    def GetRow(self, nRow, pDelim, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(26, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow, pDelim, flags)

    def GetRowID(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(29, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowTimeStamp(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(30, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowValue(self, nRow, nCol, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow, nCol, flags)

    def GetShared(self, nRow):
        return self._oleobj_.InvokeTypes(28, LCID, 1, (11, 0), ((3, 1),), nRow)

    def ModifyRow(self, nRow, nCol, pBuf, flags, ):
        return self._oleobj_.InvokeTypes(
            23,
            LCID,
            1,
            (3, 0),
            ((3, 1), (3, 1), (8, 1), (3, 1)),
            nRow,
            nCol,
            pBuf,
            flags, )

    def SetShared(self, nRow):
        return self._oleobj_.InvokeTypes(27, LCID, 1, (11, 0), ((3, 1),), nRow)

    _prop_map_get_ = {
        'ColumnCount': (2, 2, (3, 0), (), 'ColumnCount', None),
        'RowCount': (1, 2, (3, 0), (), 'RowCount', None),
    }
    _prop_map_put_ = {
        'ColumnCount': ((2, LCID, 4, 0), ()),
        'RowCount': ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        'Return a Python iterator for this object'
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return win32com.client.util.Iterator(ob, None)


class ICommenceQueryRowSet(DispatchBaseClass):
    CLSID = IID('{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    def GetColumnIndex(self, pLabel, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 1), (3, 1)), pLabel, flags)

    def GetColumnLabel(self, nCol, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(21, LCID, 1, (8, 0), ((3, 1), (3, 1)), nCol, flags)

    def GetFieldToFile(self, nRow, nCol, filename, flags, ):
        return self._oleobj_.InvokeTypes(
            26,
            LCID,
            1,
            (3, 0),
            ((3, 1), (3, 1), (8, 1), (3, 1)),
            nRow,
            nCol,
            filename,
            flags, )

    def GetRow(self, nRow, pDelim, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(23, LCID, 1, (8, 0), ((3, 1), (8, 1), (3, 1)), nRow, pDelim, flags)

    def GetRowID(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(24, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowTimeStamp(self, nRow, flags: OptionFlag = OptionFlag.NONE):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(27, LCID, 1, (8, 0), ((3, 1), (3, 1)), nRow, flags)

    def GetRowValue(self, nRow, nCol, flags, ):
        # Result is a Unicode object
        return self._oleobj_.InvokeTypes(20, LCID, 1, (8, 0), ((3, 1), (3, 1), (3, 1)), nRow, nCol, flags)

    def GetShared(self, nRow):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (11, 0), ((3, 1),), nRow)

    _prop_map_get_ = {
        'ColumnCount': (2, 2, (3, 0), (), 'ColumnCount', None),
        'RowCount': (1, 2, (3, 0), (), 'RowCount', None),
    }
    _prop_map_put_ = {
        'ColumnCount': ((2, LCID, 4, 0), ()),
        'RowCount': ((1, LCID, 4, 0), ()),
    }

    def __iter__(self):
        'Return a Python iterator for this object'
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return win32com.client.util.Iterator(ob, None)
