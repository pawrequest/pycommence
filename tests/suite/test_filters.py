"""Tests for pycommence.core.filters"""

import pytest

from pycommence.core.filters import (
    ConditionType,
    ConnectedFieldFilter,
    ConnectedItemFilter,
    FieldFilter,
    FilterArray,
    Sort,
    SortOrder,
)
from pycommence.core.types import ConnectedColumn


class TestConditionType:
    def test_equal_value(self):
        assert ConditionType.EQUAL == 'Equal To'

    def test_contain_value(self):
        assert ConditionType.CONTAIN == 'Contains'

    def test_constructable_from_string(self):
        assert ConditionType('Equal To') is ConditionType.EQUAL


class TestFieldFilter:
    def test_creation(self):
        ff = FieldFilter(column='Name', condition=ConditionType.EQUAL, value='Alice')
        assert ff.kind == 'F'
        assert ff.column == 'Name'

    def test_filter_str(self):
        ff = FieldFilter(column='Name', condition=ConditionType.EQUAL, value='Alice')
        s = ff._filter_str
        assert '"Name"' in s
        assert '"Equal To"' in s
        assert '"Alice"' in s

    def test_view_filter_str(self):
        ff = FieldFilter(column='Name', condition=ConditionType.CONTAIN, value='Bob')
        vf = ff.view_filter_str(slot=2)
        assert vf.startswith('[ViewFilter(')
        assert '"2"' in vf

    def test_to_array(self):
        ff = FieldFilter(column='x', value='y')
        arr = ff.to_array()
        assert isinstance(arr, FilterArray)
        assert len(arr.filters) == 1


class TestConnectedItemFilter:
    def test_kind(self):
        f = ConnectedItemFilter(column='Relates To', connection_category='Account', value='Acme')
        assert f.kind == 'CTI'


class TestConnectedFieldFilter:
    def test_from_fil(self):
        ff = FieldFilter(column='City', condition=ConditionType.EQUAL, value='London')
        conn = ConnectedColumn(name='Relates To', category='Account', column='City')
        cf = ConnectedFieldFilter.from_fil(ff, conn)
        assert cf.kind == 'CTCF'
        assert cf.connection_category == 'Account'


class TestFilterArray:
    def test_empty(self):
        fa = FilterArray()
        assert not fa
        assert len(fa.filters) == 0

    def test_from_filters_single(self):
        ff = FieldFilter(column='A', value='1')
        fa = FilterArray.from_filters(ff)
        assert len(fa.filters) == 1
        assert fa

    def test_from_filters_multiple(self):
        f1 = FieldFilter(column='A', value='1')
        f2 = FieldFilter(column='B', value='2')
        fa = FilterArray.from_filters(f1, f2)
        assert len(fa.filters) == 2

    def test_logics_auto_filled(self):
        f1 = FieldFilter(column='A', value='1')
        f2 = FieldFilter(column='B', value='2')
        fa = FilterArray.from_filters(f1, f2)
        assert fa.logics == ['And']

    def test_add_filter(self):
        fa = FilterArray.from_filters(FieldFilter(column='A', value='1'))
        fa.add_filter(FieldFilter(column='B', value='2'))
        assert len(fa.filters) == 2

    def test_add_filter_exceeds_max_slots(self):
        """Commence supports 8 filter slots; adding beyond 9 existing raises."""
        filters = [FieldFilter(column=f'f{i}', value=str(i)) for i in range(9)]
        fa = FilterArray.from_filters(*filters)
        with pytest.raises(ValueError, match='No empty slots'):
            fa.add_filter(FieldFilter(column='extra', value='x'))

    def test_filter_strs_returns_list(self):
        fa = FilterArray.from_filters(FieldFilter(column='A', value='1'))
        strs = fa.filter_strs
        assert isinstance(strs, list)
        assert len(strs) == 1
        assert strs[0].startswith('[ViewFilter(')

    def test_addition_both_populated(self):
        a = FilterArray.from_filters(FieldFilter(column='A', value='1'))
        b = FilterArray.from_filters(FieldFilter(column='B', value='2'))
        a + b  # mutates a in-place
        assert len(a.filters) == 2

    def test_addition_one_empty(self):
        a = FilterArray()
        b = FilterArray.from_filters(FieldFilter(column='B', value='2'))
        c = a + b
        assert c is b

    def test_str(self):
        fa = FilterArray.from_filters(FieldFilter(column='A', value='1'))
        s = str(fa)
        assert isinstance(s, str)


class TestSort:
    def test_sort_str(self):
        s = Sort(column='Name', order=SortOrder.ASC)
        assert 'Name' in str(s)
        assert 'Ascending' in str(s)

    def test_sort_order_values(self):
        assert str(SortOrder.ASC) == 'Ascending'
        assert str(SortOrder.DESC) == 'Descending'


class TestFilterArraySorts:
    def test_view_sort_text(self):
        s = Sort(column='Name', order=SortOrder.ASC)
        fa = FilterArray(sorts=[s])
        txt = fa.view_sort_text
        assert '[ViewSort(' in txt
        assert 'Name' in txt
