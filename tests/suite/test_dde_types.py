"""Tests for pycommence.dde.types"""

from pycommence.dde.types import (
    EMPTY,
    DDEExecuteGet,
    DDEExecuteView,
    DDEKind,
    DDEMessageBase,
    DDERequestGet,
    DDERequestView,
    DDESystemRequest,
    DDETopic,
    _dde_format_param,
)


class TestDDETopic:
    def test_values(self):
        assert DDETopic.VIEW == 'ViewData'
        assert DDETopic.GET == 'GetData'
        assert DDETopic.SYSTEM == 'System'


class TestDDEKind:
    def test_values(self):
        assert DDEKind.REQUEST == 'request'
        assert DDEKind.EXECUTE == 'execute'


class TestDDEFormatParam:
    def test_none_blank(self):
        assert _dde_format_param(None) == ''

    def test_bool_true(self):
        assert _dde_format_param(True) == 'yes'

    def test_bool_false(self):
        assert _dde_format_param(False) == 'no'

    def test_int(self):
        assert _dde_format_param(42) == '42'

    def test_float(self):
        assert _dde_format_param(3.14) == '3.14'

    def test_string_quoted(self):
        assert _dde_format_param('hello') == '"hello"'

    def test_string_strips_existing_quotes(self):
        assert _dde_format_param('"already"') == '"already"'


class TestDDEMessageBase:
    def test_str_no_params(self):
        msg = DDEMessageBase(func_name='GetStatus')
        assert str(msg) == '[GetStatus]'

    def test_str_with_params(self):
        msg = DDEMessageBase(func_name='GetField', params=['Contact', 'Alice', 'Name'])
        s = str(msg)
        assert s.startswith('[GetField(')
        assert '"Contact"' in s
        assert s.endswith(')]')

    def test_kind_default_request(self):
        msg = DDEMessageBase(func_name='X')
        assert msg.kind == DDEKind.REQUEST

    def test_topic_default_get(self):
        msg = DDEMessageBase(func_name='X')
        assert msg.topic == DDETopic.GET


class TestDDESystemRequest:
    def test_str_format(self):
        msg = DDESystemRequest(func_name='Status')
        assert str(msg) == 'Status'

    def test_topic(self):
        msg = DDESystemRequest(func_name='Status')
        assert msg.topic == DDETopic.SYSTEM


class TestDDESubclasses:
    def test_request_get_defaults(self):
        msg = DDERequestGet(func_name='X')
        assert msg.kind == DDEKind.REQUEST
        assert msg.topic == DDETopic.GET

    def test_request_view_defaults(self):
        msg = DDERequestView(func_name='X')
        assert msg.kind == DDEKind.REQUEST
        assert msg.topic == DDETopic.VIEW

    def test_execute_get_defaults(self):
        msg = DDEExecuteGet(func_name='X')
        assert msg.kind == DDEKind.EXECUTE
        assert msg.topic == DDETopic.GET

    def test_execute_view_defaults(self):
        msg = DDEExecuteView(func_name='X')
        assert msg.kind == DDEKind.EXECUTE
        assert msg.topic == DDETopic.VIEW


class TestEmpty:
    def test_empty_is_string(self):
        assert EMPTY == 'empty'
