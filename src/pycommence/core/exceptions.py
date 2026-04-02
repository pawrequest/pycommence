from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    pass


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


class HasRowCount(Protocol):
    @property
    def row_count(self) -> int: ...


def raise_for_one(res: HasRowCount):
    if res.row_count == 0:
        raise PyCommenceNotFoundError('Row not found.')
    if res.row_count > 1:
        raise PyCommenceMaxExceededError('Multiple rows found')
