"""Tests for pycommence.core.types"""

from datetime import date, datetime

import pytest

from pycommence.core.types import (
    ConnectedColumn,
    Connection,
    get_cmc_date_maybe,
    join_csv,
    replace_noncompliant_apostrophes,
    split_csv,
    to_cmc_date,
)


class TestGetCmcDateMaybe:
    def test_from_date(self):
        d = date(2024, 1, 15)
        assert get_cmc_date_maybe(d) == d

    def test_from_datetime(self):
        dt = datetime(2024, 1, 15, 10, 30)
        assert get_cmc_date_maybe(dt) == date(2024, 1, 15)

    def test_from_canonical_str(self):
        assert get_cmc_date_maybe('20240115') == date(2024, 1, 15)

    def test_from_iso_str(self):
        assert get_cmc_date_maybe('2024-01-15') == date(2024, 1, 15)

    def test_none_for_garbage(self):
        assert get_cmc_date_maybe('hello') is None

    def test_none_returns_none(self):
        assert get_cmc_date_maybe(None) is None


class TestToCmcDate:
    def test_date_to_str(self):
        assert to_cmc_date(date(2024, 3, 5)) == '20240305'

    def test_none_gives_empty(self):
        assert to_cmc_date(None) == ''


class TestReplaceApostrophes:
    def test_smart_quotes(self):
        assert replace_noncompliant_apostrophes('\u2018hello\u2019') == "'hello'"

    def test_normal_quote_unchanged(self):
        assert replace_noncompliant_apostrophes("it's") == "it's"

    def test_none_returns_none_string(self):
        # str(None) -> 'None'; the function does str(value) first
        assert replace_noncompliant_apostrophes(None) == 'None'


class TestSplitCsv:
    def test_string(self):
        assert split_csv('a, b, c') == ['a', 'b', 'c']

    def test_list_passthrough(self):
        assert split_csv(['a', 'b']) == ['a', 'b']

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            split_csv(123)


class TestJoinCsv:
    def test_list(self):
        assert join_csv(['a', 'b', 'c']) == 'a, b, c'

    def test_string_passthrough(self):
        assert join_csv('already') == 'already'

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError):
            join_csv(123)


class TestDataclasses:
    def test_connection(self):
        c = Connection(name='rel', from_table='A', from_field='af', to_table='B', to_field='bf')
        assert c.name == 'rel'

    def test_connected_column(self):
        cc = ConnectedColumn(name='Relates To', category='Account', column='City')
        assert cc.category == 'Account'
