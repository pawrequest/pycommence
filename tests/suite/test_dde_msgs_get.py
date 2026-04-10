"""Tests for pycommence.dde.msgs.get – message construction"""

from pycommence.dde.msgs import get
from pycommence.dde.types import DDEKind


class TestGetMessages:
    def test_category_count(self):
        msg = get.category_count()
        assert msg.func_name == 'GetCategoryCount'
        assert msg.kind == DDEKind.REQUEST

    def test_category_names(self):
        msg = get.category_names()
        assert 'GetCategoryNames' in str(msg)

    def test_field_names(self):
        msg = get.field_names('Contact')
        assert 'GetFieldNames' in str(msg)
        assert '"Contact"' in str(msg)

    def test_field_definition(self):
        msg = get.field_definition('Contact', 'firstName')
        assert 'GetFieldDefinition' in str(msg)

    def test_field(self):
        msg = get.field('Contact', 'Alice', 'Name')
        assert msg.func_name == 'GetField'

    def test_fields(self):
        msg = get.fields('Contact', 'Alice', ['Name', 'City'])
        s = str(msg)
        assert 'GetFields' in s
        assert '2' in s  # field count

    def test_item_count(self):
        msg = get.item_count('Contact')
        assert msg.returns == [int]

    def test_item_names(self):
        msg = get.item_names('Contact')
        assert 'GetItemNames' in str(msg)

    def test_database(self):
        msg = get.database()
        assert 'GetDatabase' in str(msg)

    def test_connection_names(self):
        msg = get.connection_names('Contact')
        assert 'GetConnectionNames' in str(msg)

    def test_view_names(self):
        msg = get.view_names('Contact')
        assert 'GetViewNames' in str(msg)

    def test_last_error(self):
        msg = get.last_error()
        assert msg.func_name == 'GetLastError'

    def test_clarify_item_names_query(self):
        msg = get.clarify_item_names()
        assert msg.func_name == 'ClarifyItemNames'
        assert msg.params == []

    def test_clarify_item_names_set(self):
        msg = get.clarify_item_names(True)
        assert msg.params == [True]
