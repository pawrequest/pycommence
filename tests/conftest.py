import contextlib
from typing import ClassVar, ContextManager

import pytest
from loguru import logger
from pydantic import Field
from sample_data import TEST_ITEM_NAME

from pycommence.core.meta import CommenceTable
from pycommence.dde import DDETopic
from pycommence.pycommence_client import PyCommence
from pycommence.testing import test_client, test_client_non_tutorial


class Contact(CommenceTable):
    category: ClassVar[str] = 'Contact'
    name: str = Field(..., alias='contactKey')
    firstName: str


class Account(CommenceTable):
    category: ClassVar[str] = 'Account'
    name: str = Field(..., alias='accountKey')


@pytest.fixture(scope='function')
def timed():
    from time import time

    start = time()
    yield
    end = time()
    logger.debug(f'Test took {end - start:.4f} seconds')


@pytest.fixture(scope='function', autouse=True)
def delay_log(caplog):
    with caplog.at_level('DEBUG'):
        yield
    print('\n\nCaptured logs:')
    for record in caplog.records:
        print(f'{record.levelname}: {record.message}')


@pytest.fixture(scope='function')
def contact_cursor(test_client):
    yield test_client.cursor('Contact')


@contextlib.contextmanager
def temp_contact(client: PyCommence, category='Contact') -> ContextManager[PyCommence]:
    topic = DDETopic.GET
    try:
        res = client.item_add_dde(category, TEST_ITEM_NAME, DDETopic.GET)
        assert res is True
        yield client

    finally:
        logger.info('Cleaning up temp contact')
        assert client.item_delete_dde(category, TEST_ITEM_NAME, DDETopic.GET) is True


__all__ = [
    'test_client',
    'test_client_non_tutorial',
]
