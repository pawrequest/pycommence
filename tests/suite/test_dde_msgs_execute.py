"""Tests for pycommence.dde.msgs.execute"""

import pytest

from pycommence.dde.msgs import execute
from pycommence.dde.types import DDEKind, DDETopic


class TestExecuteMessages:
    def test_add_item(self):
        msg = execute.add_item('Contact', 'Alice', DDETopic.GET)
        assert msg.func_name == 'AddItem'
        assert msg.kind == DDEKind.EXECUTE

    def test_delete_item(self):
        msg = execute.delete_item('Contact', 'Alice', DDETopic.GET)
        assert msg.func_name == 'DeleteItem'

    def test_edit_item(self):
        msg = execute.edit_item('Contact', 'Alice', 'City', 'London', DDETopic.GET)
        assert msg.func_name == 'EditItem'

    def test_assign_connection(self):
        msg = execute.assign_connection('Contact', 'Alice', 'Relates To', 'Account', 'Acme', DDETopic.GET)
        assert msg.func_name == 'AssignConnection'

    def test_unassign_connection(self):
        msg = execute.unassign_connection('Contact', 'Alice', 'Relates To', 'Account', 'Acme', DDETopic.GET)
        assert msg.func_name == 'UnassignConnection'

    def test_fire_trigger(self):
        msg = execute.fire_trigger('MyTrigger', 'a', 'b', topic=DDETopic.GET)
        assert msg.func_name == 'FireTrigger'

    def test_fire_trigger_too_many_args(self):
        with pytest.raises(ValueError):
            execute.fire_trigger('T', *['a'] * 9, topic=DDETopic.GET)

    def test_log_phone_call_odd_args(self):
        with pytest.raises(ValueError):
            execute.log_phone_call('Contact')

    def test_log_phone_call(self):
        msg = execute.log_phone_call('Contact', 'Alice')
        assert msg.func_name == 'LogPhoneCall'

    def test_show_item(self):
        msg = execute.show_item('Contact', 'Alice', DDETopic.GET)
        assert msg.func_name == 'ShowItem'

    def test_show_view(self):
        msg = execute.show_view('MyView', DDETopic.GET)
        assert msg.func_name == 'ShowView'
