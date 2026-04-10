"""Tests for pycommence.dde.msgs.view"""

import pytest

from pycommence.dde.msgs import view


class TestViewMessages:
    def test_category(self):
        msg = view.category('Contact')
        assert msg.func_name == 'ViewCategory'

    def test_item_count(self):
        msg = view.item_count()
        assert msg.func_name == 'ViewItemCount'

    def test_field(self):
        msg = view.field(0, 'Name')
        assert msg.func_name == 'ViewField'

    def test_fields(self):
        msg = view.fields(0, ['Name', 'City'])
        assert msg.func_name == 'ViewFields'

    def test_sort_odd_args_raises(self):
        with pytest.raises(ValueError):
            view.sort('Name')

    def test_sort_too_many_raises(self):
        with pytest.raises(ValueError):
            view.sort(*['f', 'Ascending'] * 5)

    def test_sort_valid(self):
        msg = view.sort('Name', 'Ascending')
        assert msg.func_name == 'ViewSort'

    def test_mark_item(self):
        msg = view.mark_item(0)
        assert msg.func_name == 'ViewMarkItem'

    def test_connected_count(self):
        msg = view.connected_count(0, 'Relates To', 'Account')
        assert msg.func_name == 'ViewConnectedCount'
