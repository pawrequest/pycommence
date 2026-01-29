import contextlib
import threading
from typing import ClassVar, ContextManager
from collections.abc import Generator

from loguru import logger
import pytest

from pycommence.threads import com_context
from pycommence.pycommence_client import PyCommenceClient
from pycommence import PyCmcDDEServer
from pycommence.dde.server import DDEMessageBase
from pycommence.core.fields import DELIM
from sample_data import TEST_ITEM_NAME
from pycommence.core.meta import CommenceTableGenerated
from bench.client import PyCommence
from pycommence.dde import DDETopic


@pytest.fixture(scope='function', autouse=True)
def delay_log(caplog):
    with caplog.at_level('DEBUG'):
        yield
    for record in caplog.records:
        print(f'{record.levelname}: {record.message}')


@pytest.mark.asyncio
def get_pycmc(tblname: str | None = None):
    pycmc = PyCommence()
    if tblname:
        pycmc.set_csr(csrname=tblname)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


@pytest.fixture(scope='function')
def pycmc():
    return get_pycmc('Contact')


@pytest.fixture(scope='function')
def pycmc_no_csr() -> PyCommence:
    return get_pycmc()


class Contact(CommenceTableGenerated):
    category: ClassVar[str] = 'Contact'
    name_field: ClassVar[str] = 'contactKey'


class Account(CommenceTableGenerated):
    category: ClassVar[str] = 'Account'
    name_field: ClassVar[str] = 'accountKey'


@pytest.fixture(scope='function')
def dde_server_old() -> Generator[PyCmcDDEServer, None, None]:
    thread_id = threading.get_ident()
    logger.warning(f'DDEServer fixture running in thread {thread_id}')
    # inititialized = False
    with PyCmcDDEServer() as server:
        try:
            msg = DDEMessageBase(func_name='GetDatabase', params=[DELIM])
            assert server.send_message(msg)[0] == 'Tutorial', 'Must Use Tutorial DB'
            yield server

        finally:
            ...
            # if inititialized:
            #     comtypes.CoUninitialize()


@pytest.fixture(scope='function')
def pycmc_client():
    with com_context(), PyCommenceClient() as client:
        yield client


@pytest.fixture(scope='function')
def contact_cursor(pycmc_client):
    yield pycmc_client.cursor('Contact')


# @contextlib.contextmanager
# def temp_contact_dde(server: PyCmcDDEServer, category='Contact') -> ContextManager[
#     PyCmcDDEServer]:  # prefer the pycharm false positive here to in callers
#     try:
#         assert server.item_add(category, TEST_ITEM_NAME, DDETopic.GET) is True
#         yield server
#
#     finally:
#         logger.info('Cleaning up temp contact')
#         assert server.item_delete(category, TEST_ITEM_NAME, DDETopic.GET) is True


@contextlib.contextmanager
def temp_contact(client: PyCommenceClient, category='Contact') -> ContextManager[
    PyCommenceClient]:  # prefer the pycharm false positive here to in callers
    topic = DDETopic.GET
    try:
        res = client.item_add(category, TEST_ITEM_NAME, DDETopic.GET)
        assert res is True
        yield client

    finally:
        logger.info('Cleaning up temp contact')
        assert client.item_delete(category, TEST_ITEM_NAME, DDETopic.GET) is True
