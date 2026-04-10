"""Integration tests for PyCommence client (requires live Commence)."""

import pytest

from pycommence.conversation import ConversationAPI
from pycommence.cursor import CursorAPI
from pycommence.dde import DDETopic
from pycommence.icommence.const import CursorType
from pycommence.pycommence_client import PyCommence

pytestmark = pytest.mark.integration


class TestPyCommenceClient:
    def test_context_manager(self, com_ctx):
        with PyCommence() as client:
            assert client is not None

    def test_cursor_creation(self, pycmc: PyCommence):
        csr = pycmc.cursor('Contact')
        assert isinstance(csr, CursorAPI)

    def test_cursor_cached(self, pycmc: PyCommence):
        c1 = pycmc.cursor('Contact')
        c2 = pycmc.cursor('Contact')
        assert c1 is c2

    def test_conversation(self, pycmc: PyCommence):
        conv = pycmc.conversation()
        assert isinstance(conv, ConversationAPI)

    def test_create_cursor_requires_name(self, pycmc: PyCommence):
        with pytest.raises(ValueError):
            pycmc.create_cursor(name=None, mode=CursorType.CATEGORY)

    def test_pilot_and_internet_exclusive(self, pycmc: PyCommence):
        with pytest.raises(ValueError):
            pycmc.create_cursor(name='X', pilot=True, internet=True)


class TestPyCommenceDDE:
    def test_item_read_dde(self, pycmc: PyCommence, temp_contact: str):
        result = pycmc.item_read_dde('Contact', temp_contact)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_item_read_dde_specific_fields(self, pycmc: PyCommence, temp_contact: str):
        result = pycmc.item_read_dde('Contact', temp_contact, fields=['firstName', 'lastName'])
        assert 'firstName' in result
        assert 'lastName' in result
        assert len(result) == 2

    def test_item_edit_dde(self, pycmc: PyCommence, temp_contact: str):
        result = pycmc.item_edit_dde(
            'Contact',
            temp_contact,
            {'firstName': 'DDEEdited'},
            DDETopic.GET,
        )
        assert result is True
        data = pycmc.item_read_dde('Contact', temp_contact, fields=['firstName'])
        assert data['firstName'] == 'DDEEdited'
