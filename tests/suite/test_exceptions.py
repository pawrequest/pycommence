"""Tests for pycommence.core.exceptions"""

import pytest

from pycommence.core.exceptions import (
    Handle,
    PyCommenceError,
    PyCommenceExistsError,
    PyCommenceMaxExceededError,
    PyCommenceNotFoundError,
    PyCommenceServerError,
    raise_for_one,
)


class _FakeRowSet:
    def __init__(self, n):
        self._n = n

    @property
    def row_count(self):
        return self._n


class TestRaiseForOne:
    def test_zero_raises_not_found(self):
        with pytest.raises(PyCommenceNotFoundError):
            raise_for_one(_FakeRowSet(0))

    def test_one_ok(self):
        raise_for_one(_FakeRowSet(1))  # should not raise

    def test_multiple_raises_max_exceeded(self):
        with pytest.raises(PyCommenceMaxExceededError):
            raise_for_one(_FakeRowSet(3))


class TestExceptionHierarchy:
    def test_exists_is_pycommence_error(self):
        assert issubclass(PyCommenceExistsError, PyCommenceError)

    def test_not_found_is_pycommence_error(self):
        assert issubclass(PyCommenceNotFoundError, PyCommenceError)

    def test_max_exceeded_is_pycommence_error(self):
        assert issubclass(PyCommenceMaxExceededError, PyCommenceError)

    def test_server_error_is_pycommence_error(self):
        assert issubclass(PyCommenceServerError, PyCommenceError)


class TestHandle:
    def test_values(self):
        assert Handle.IGNORE == 'ignore'
        assert Handle.RAISE == 'raise'
        assert Handle.UPDATE == 'update'
        assert Handle.REPLACE == 'replace'
        assert Handle.ALL == 'all'
