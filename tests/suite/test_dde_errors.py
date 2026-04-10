"""Tests for pycommence.dde.dde_errors"""

import pytest

from pycommence.dde.dde_errors import (
    PyCmcDDEError,
    PyCmcDDENoConnectionError,
    dde_error_code_lookup,
    raise_for_bad_dde,
)


class TestDDEErrorCodeLookup:
    def test_known_code(self):
        assert 'memory' in dde_error_code_lookup(100).lower()

    def test_field_position_error(self):
        msg = dde_error_code_lookup(3)
        assert 'position 3' in msg.lower()

    def test_unknown_code(self):
        msg = dde_error_code_lookup(9999)
        assert 'unknown' in msg.lower()


class TestPyCmcDDEError:
    def test_creation(self):
        err = PyCmcDDEError(cmd='TestCmd', code=100)
        assert err.code == 100
        assert err.cmd == 'TestCmd'

    def test_custom_msg(self):
        err = PyCmcDDEError(cmd='X', code=0, msg='custom')
        assert str(err) == 'custom'


class TestPyCmcDDENoConnectionError:
    def test_default_msg(self):
        err = PyCmcDDENoConnectionError()
        assert 'connection failed' in str(err).lower()


class TestRaiseForBadDde:
    def test_active_item_not_found(self):
        with pytest.raises(PyCmcDDEError):
            raise_for_bad_dde('cmd', '(Active item not found)')

    def test_normal_value_ok(self):
        raise_for_bad_dde('cmd', 'Alice')  # should not raise

    def test_bool_ok(self):
        raise_for_bad_dde('cmd', True)  # should not raise
