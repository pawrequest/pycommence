from __future__ import annotations


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
