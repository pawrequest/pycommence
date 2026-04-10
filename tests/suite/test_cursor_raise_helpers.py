"""Tests for cursor-level helper functions."""

import pytest

from pycommence.cursor import raise_for_id_or_pk


class TestRaiseForIdOrPk:
    def test_both_none_raises(self):
        with pytest.raises(ValueError):
            raise_for_id_or_pk(None, None)

    def test_id_only_ok(self):
        raise_for_id_or_pk('some_id', None)

    def test_pk_only_ok(self):
        raise_for_id_or_pk(None, 'some_pk')

    def test_both_ok(self):
        raise_for_id_or_pk('id', 'pk')
