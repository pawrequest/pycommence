"""Integration tests for the MCP server tools (requires live Commence).

These tests import the tool functions directly and call them in-process
(no stdio transport needed).
"""

import json

import pytest

pytestmark = pytest.mark.integration


class TestMCPListCategories:
    def test_returns_json_list(self, com_ctx):
        from mcp_server import list_categories

        # MCP tool functions return strings
        # We need to call within COM context
        from pycommence.threads import com_context

        with com_context():
            result = list_categories()
        data = json.loads(result)
        assert isinstance(data, list)
        assert 'Contact' in data


class TestMCPGetFieldNames:
    def test_contact_fields(self, com_ctx):
        from mcp_server import get_category_field_names
        from pycommence.threads import com_context

        with com_context():
            result = get_category_field_names('Contact')
        data = json.loads(result)
        assert isinstance(data, list)
        assert 'contactKey' in data
        assert 'firstName' in data


class TestMCPGetFieldDefinitions:
    def test_contact_definitions(self, com_ctx):
        from mcp_server import get_category_field_definitions
        from pycommence.threads import com_context

        with com_context():
            result = get_category_field_definitions('Contact')
        data = json.loads(result)
        assert isinstance(data, dict)
        assert len(data) > 0


class TestMCPRowCount:
    def test_contact_count(self, com_ctx):
        from mcp_server import get_row_count
        from pycommence.threads import com_context

        with com_context():
            result = get_row_count('Contact')
        assert int(result) >= 0


class TestMCPReadRows:
    def test_read_rows(self, com_ctx):
        from mcp_server import read_rows
        from pycommence.threads import com_context

        with com_context():
            result = read_rows('Contact', limit=3)
        data = json.loads(result)
        assert isinstance(data, list)
        assert len(data) <= 3


class TestMCPGetDbName:
    def test_db_name(self, com_ctx):
        from mcp_server import get_db_name
        from pycommence.threads import com_context

        with com_context():
            result = get_db_name()
        data = json.loads(result)
        assert 'name' in data or isinstance(data, str)
