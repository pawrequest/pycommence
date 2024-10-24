from __future__ import annotations

from enum import StrEnum
from typing import Protocol

from loguru import logger


class CmcError(Exception):
    def __init__(self, msg: str = ''):
        self.msg = msg
        super().__init__(self.msg)


class PyCommenceError(Exception):
    pass


class PyCommenceExistsError(PyCommenceError):
    pass


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
