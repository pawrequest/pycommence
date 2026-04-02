import contextlib
from typing import ClassVar, ContextManager

import pytest
from loguru import logger
from sample_data import TEST_ITEM_NAME

from pycommence.core.meta import CommenceTable
from pycommence.dde import DDETopic
from pycommence.pycommence_client import PyCommenceClient
from pycommence.threads import com_context


class Contact(CommenceTable):
    category: ClassVar[str] = 'Contact'
    name_field: ClassVar[str] = 'contactKey'
    firstName: str


class Account(CommenceTable):
    category: ClassVar[str] = 'Account'
    name_field: ClassVar[str] = 'accountKey'


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
def pycmc():
    with com_context(), PyCommenceClient() as client:
        if not client.conversation().db_name_and_path()[0] == 'Tutorial':
            raise ValueError('Expected Tutorial DB')
        yield client
    # return get_pycmc('Contact')


@pytest.fixture(scope='function')
def pycmc_client():
    with com_context(), PyCommenceClient() as client:
        yield client


@pytest.fixture(scope='function')
def contact_cursor(pycmc_client):
    yield pycmc_client.cursor('Contact')


@contextlib.contextmanager
def temp_contact(
    client: PyCommenceClient, category='Contact'
) -> ContextManager[PyCommenceClient]:  # prefer the pycharm false positive here to in callers
    topic = DDETopic.GET
    try:
        res = client.item_add_dde(category, TEST_ITEM_NAME, DDETopic.GET)
        assert res is True
        yield client

    finally:
        logger.info('Cleaning up temp contact')
        assert client.item_delete_dde(category, TEST_ITEM_NAME, DDETopic.GET) is True
