"""conftest.py - Shared fixtures for the pycommence test-suite."""

from __future__ import annotations

import contextlib
import uuid
from typing import ContextManager

import pytest
from loguru import logger

from pycommence.dde import DDETopic
from pycommence.pycommence_client import PyCommence
from pycommence.threads import com_context

TEST_ITEM_PREFIX = '_PyCmcTest_'


def _unique_item_name() -> str:
    return f'{TEST_ITEM_PREFIX}{uuid.uuid4().hex[:8]}'


@pytest.fixture(scope='session')
def com_ctx():
    with com_context():
        yield


@pytest.fixture(scope='session')
def pycmc(com_ctx):
    with PyCommence() as client:
        yield client


@pytest.fixture()
def contact_cursor(pycmc: PyCommence):
    return pycmc.cursor('Contact')


@pytest.fixture()
def account_cursor(pycmc: PyCommence):
    return pycmc.cursor('Account')


@contextlib.contextmanager
def temp_item(client: PyCommence, category: str = 'Contact') -> ContextManager[str]:
    name = _unique_item_name()
    topic = DDETopic.GET
    try:
        res = client.item_add_dde(category, name, topic)
        assert res is True, f'Failed to add temp item {name!r}'
        yield name
    finally:
        logger.info(f'Cleaning up temp item {name!r}')
        client.item_delete_dde(category, name, topic)


@pytest.fixture()
def temp_contact(pycmc: PyCommence):
    with temp_item(pycmc, 'Contact') as name:
        yield name


@pytest.fixture(autouse=True)
def _log_test_name(request):
    logger.info(f'>>> {request.node.nodeid}')
    yield
    logger.info(f'<<< {request.node.nodeid}')
