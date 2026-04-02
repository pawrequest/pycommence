from typing import TYPE_CHECKING, cast

import pythoncom
from loguru import logger
from win32.lib.pywintypes import IID
from win32com import client
from win32com.client import Dispatch, DispatchBaseClass

if TYPE_CHECKING:
    from pycommence.icommence.row import (
        ICommenceAddRowSet,
        ICommenceDeleteRowSet,
        ICommenceEditRowSet,
        ICommenceQueryRowSet,
    )
from pycommence.icommence.const import LCID, OptionFlag


def default_flags(default=OptionFlag.NONE):
    logger.debug(f'Creating default_flags decorator with default={default}')
    logger.debug(f'Creating default_flags decorator with default={default}')
    logger.debug(f'Creating default_flags decorator with default={default}')

    def decorator(func):
        logger.debug(f'Decorating {func.__name__} with default flags={default}')

        def wrapper(self, *args, **kwargs):
            logger.debug(f'Calling {func.__name__} with args={args}, kwargs={kwargs}')
            # If flags is missing, append default
            if len(args) < func.__code__.co_argcount - 1:
                args = args + (default,)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


class ICommenceCursor(DispatchBaseClass):
    CLSID = IID('{C5D7DAE0-9BEC-11D1-99CC-00C04FD3695E}')
    coclass_clsid = None

    # Result is of type ICommenceAddRowSet
    def GetAddRowSet(self, nCount, flags) -> 'ICommenceAddRowSet':
        ret = self._oleobj_.InvokeTypes(28, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetAddRowSet', '{C5D7DAE3-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceDeleteRowSet
    def GetDeleteRowSet(self, nCount, flags) -> 'ICommenceDeleteRowSet':
        ret = self._oleobj_.InvokeTypes(31, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetDeleteRowSet', '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceDeleteRowSet
    def GetDeleteRowSetByID(self, pRowID, flags) -> 'ICommenceDeleteRowSet':
        ret = self._oleobj_.InvokeTypes(32, LCID, 1, (9, 0), ((8, 1), (3, 1)), pRowID, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetDeleteRowSetByID', '{C5D7DAE5-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    # Result is of type ICommenceEditRowSet
    def GetEditRowSet(self, nCount, flags) -> 'ICommenceEditRowSet':
        ret = self._oleobj_.InvokeTypes(29, LCID, 1, (9, 0), ((3, 1), (3, 1)), nCount, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetEditRowSet', '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetEditRowSetByID(self, row_id: str, flags: OptionFlag = OptionFlag.NONE) -> 'ICommenceEditRowSet':
        ret = self._oleobj_.InvokeTypes(30, LCID, 1, (9, 0), ((8, 1), (3, 1)), row_id, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetEditRowSetByID', '{C5D7DAE4-9BEC-11D1-99CC-00C04FD3695E}')
        return ret

    def GetQueryRowSet(self, count: int, flags: OptionFlag = OptionFlag.NONE) -> 'ICommenceQueryRowSet':
        ret = self._oleobj_.InvokeTypes(26, LCID, 1, (9, 0), ((3, 1), (3, 1)), count, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetQueryRowSet', '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
        return cast('ICommenceQueryRowSet', cast(object, ret))

    # Result is of type ICommenceQueryRowSet
    def GetQueryRowSetByID(self, pRowID, flags) -> 'ICommenceQueryRowSet':
        ret = self._oleobj_.InvokeTypes(27, LCID, 1, (9, 0), ((8, 1), (3, 1)), pRowID, flags)
        if ret is not None:
            ret = Dispatch(ret, 'GetQueryRowSetByID', '{C5D7DAE2-9BEC-11D1-99CC-00C04FD3695E}')
        return cast('ICommenceQueryRowSet', cast(object, ret))

    def SeekRow(self, bkOrigin, nRows):
        return self._oleobj_.InvokeTypes(24, LCID, 1, (3, 0), ((3, 1), (3, 1)), bkOrigin, nRows)

    def SeekRowApprox(self, nNumerator, nDenom):
        return self._oleobj_.InvokeTypes(25, LCID, 1, (3, 0), ((3, 1), (3, 1)), nNumerator, nDenom)

    def SetActiveDate(self, sDate, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(34, LCID, 1, (11, 0), ((8, 1), (3, 1)), sDate, flags)

    def SetActiveDateRange(self, startDate, endDate, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(35, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), startDate, endDate, flags)

    def SetActiveItem(self, pCategoryName, pRowID, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(33, LCID, 1, (11, 0), ((8, 1), (8, 1), (3, 1)), pCategoryName, pRowID, flags)

    def SetColumn(self, nColumn, pName, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(23, LCID, 1, (11, 0), ((3, 1), (8, 1), (3, 1)), nColumn, pName, flags)

    def SetFilter(self, pFilter, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(20, LCID, 1, (11, 0), ((8, 1), (3, 1)), pFilter, flags)

    def SetLogic(self, pLogic, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(21, LCID, 1, (11, 0), ((8, 1), (3, 1)), pLogic, flags)

    def SetRelatedColumn(
        self,
        nColumn,
        pConnName,
        pCatName,
        pName,
        flags,
    ):
        return self._oleobj_.InvokeTypes(
            36,
            LCID,
            1,
            (11, 0),
            ((3, 1), (8, 1), (8, 1), (8, 1), (3, 1)),
            nColumn,
            pConnName,
            pCatName,
            pName,
            flags,
        )

    def SetSort(self, pSort, flags: OptionFlag = OptionFlag.NONE):
        return self._oleobj_.InvokeTypes(22, LCID, 1, (11, 0), ((8, 1), (3, 1)), pSort, flags)

    _prop_map_get_ = {
        'Category': (1, 2, (8, 0), (), 'Category', None),
        'ColumnCount': (3, 2, (3, 0), (), 'ColumnCount', None),
        'MaxFieldSize': (5, 2, (3, 0), (), 'MaxFieldSize', None),
        'MaxRows': (6, 2, (3, 0), (), 'MaxRows', None),
        'RowCount': (2, 2, (3, 0), (), 'RowCount', None),
        'Shared': (4, 2, (11, 0), (), 'Shared', None),
    }
    _prop_map_put_ = {
        'Category': ((1, LCID, 4, 0), ()),
        'ColumnCount': ((3, LCID, 4, 0), ()),
        'MaxFieldSize': ((5, LCID, 4, 0), ()),
        'MaxRows': ((6, LCID, 4, 0), ()),
        'RowCount': ((2, LCID, 4, 0), ()),
        'Shared': ((4, LCID, 4, 0), ()),
    }

    def __iter__(self):
        "Return a Python iterator for this object"
        try:
            ob = self._oleobj_.InvokeTypes(-4, LCID, 3, (13, 10), ())
        except pythoncom.error:
            raise TypeError('This object does not support enumeration')
        return client.util.Iterator(ob, None)
