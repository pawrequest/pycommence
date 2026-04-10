"""Integration tests for ConversationAPI (requires live Commence)."""

import pytest

from pycommence.pycommence_client import PyCommence

pytestmark = pytest.mark.integration


class TestConversationFieldNames:
    def test_contact_field_names_returns_list(self, pycmc: PyCommence):
        names = pycmc.conversation().category_field_names('Contact')
        assert isinstance(names, list)
        assert len(names) > 0

    def test_contact_has_contactkey(self, pycmc: PyCommence):
        names = pycmc.conversation().category_field_names('Contact')
        assert 'contactKey' in names

    def test_contact_has_firstname(self, pycmc: PyCommence):
        names = pycmc.conversation().category_field_names('Contact')
        assert 'firstName' in names


class TestConversationFieldDefinitions:
    def test_returns_dict(self, pycmc: PyCommence):
        defs = pycmc.conversation().category_field_definitions('Contact')
        assert isinstance(defs, dict)
        assert len(defs) > 0

    def test_definition_has_type(self, pycmc: PyCommence):
        defs = pycmc.conversation().category_field_definitions('Contact')
        first_def = next(iter(defs.values()))
        assert hasattr(first_def, 'type')


class TestConversationDbName:
    def test_db_name_and_path(self, pycmc: PyCommence):
        result = pycmc.conversation().db_name_and_path()
        assert result is not None
        # Result should be a list of [name, path] or a string
        if isinstance(result, list):
            assert len(result) == 2
