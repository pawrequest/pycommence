"""
MCP server exposing pycommence read-only tools for the Commence Tutorial DB.

Run with:  python mcp_server.py
Registered in mcp.json as a stdio server.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any

from mcp.server.fastmcp import FastMCP

from pycommence.core.filters import ConditionType, FieldFilter, FilterArray
from pycommence.core.pagination import Pagination
from pycommence.pycommence_client import PyCommence
from pycommence.threads import com_context

mcp = FastMCP('pycommence-db')

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@contextmanager
def _client():
    """Yield a connected PyCommence client inside a proper COM context."""
    with com_context(), PyCommence() as client:
        yield client


def _rows_to_dicts(
    client: PyCommence, category: str, pagination: Pagination, filter_array: FilterArray | None = None
) -> list[dict[str, Any]]:
    rows = client.cursor(category).read_rows(pagination=pagination, filter_array=filter_array)
    results = []
    for row in rows:
        # MoreAvailable sentinel – skip
        if not hasattr(row, 'data'):
            continue
        results.append(row.data)
    return results


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def list_categories() -> str:
    """List every category (table) name in the open Commence database."""
    from pycommence.dde import msgs

    with _client() as client:
        conv = client.conversation()
        raw = conv.send_message(msgs.get.category_names())
        if isinstance(raw, list):
            return json.dumps(raw, indent=2)
        return str(raw)


@mcp.tool()
def get_category_field_names(category: str) -> str:
    """Return the field (column) names for a Commence category."""
    with _client() as client:
        names = client.conversation().category_field_names(category)
        if isinstance(names, list):
            return json.dumps(names, indent=2)
        return str(names)


@mcp.tool()
def get_category_field_definitions(category: str) -> str:
    """Return field definitions (name, type, max-length …) for a Commence category."""
    with _client() as client:
        defs = client.conversation().category_field_definitions(category)
        return json.dumps({k: str(v) for k, v in defs.items()}, indent=2)


@mcp.tool()
def get_row_count(category: str) -> str:
    """Return the number of rows in a Commence category."""
    with _client() as client:
        count = client.cursor(category).row_count
        return str(count)


@mcp.tool()
def read_rows(category: str, limit: int = 20, offset: int = 0) -> str:
    """Read rows from a Commence category with optional pagination.

    Args:
        category: Commence category name (e.g. 'Contact', 'Account').
        limit: Maximum rows to return (default 20).
        offset: Row offset for pagination (default 0).
    """
    with _client() as client:
        data = _rows_to_dicts(client, category, Pagination(offset=offset, limit=limit))
        return json.dumps(data, indent=2)


@mcp.tool()
def read_row_by_pk(category: str, pk_value: str) -> str:
    """Read a single row from a Commence category by its primary-key value.

    Args:
        category: Commence category name.
        pk_value: The primary-key value identifying the row.
    """
    with _client() as client:
        row = client.cursor(category).read_row(pk=pk_value)
        return json.dumps(row.data, indent=2)


@mcp.tool()
def search_rows(category: str, field: str, value: str, condition: str = 'Contains', limit: int = 50) -> str:
    """Search rows in a Commence category by a field condition.

    Args:
        category: Commence category name.
        field: Field name to filter on.
        value: Value to compare against.
        condition: One of 'Equal To', 'Contains', 'After', 'Before', etc.
        limit: Max rows returned.
    """
    cond = ConditionType(condition)
    fil = FilterArray.from_filters(FieldFilter(column=field, condition=cond, value=value))
    with _client() as client:
        data = _rows_to_dicts(client, category, Pagination(limit=limit), filter_array=fil)
        return json.dumps(data, indent=2)


@mcp.tool()
def get_db_name() -> str:
    """Return the name and path of the currently open Commence database."""
    with _client() as client:
        info = client.conversation().db_name_and_path()
        if isinstance(info, list):
            return json.dumps({'name': info[0], 'path': info[1]}, indent=2)
        return str(info)


if __name__ == '__main__':
    mcp.run(transport='stdio')
