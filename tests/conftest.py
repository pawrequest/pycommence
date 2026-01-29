import contextlib
import threading
from typing import ClassVar
from collections.abc import Generator

import comtypes
import pytest
from loguru import logger

from pycommence import PyCmcDDEServer
from pycommence.dde.server import DDEMessageBase, DDETopic
from pycommence.core.meta import CommenceTableGenerated
from pycommence.core.fields import DELIM
from pycommence.com.client import PyCommence
from sample_data import TEST_ITEM_NAME


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
def dde_serverunsafe() -> Generator[PyCmcDDEServer]:
    thread_id = threading.get_ident()
    logger.warning(f'DDEServer fixture running in thread {thread_id}')
    with PyCmcDDEServer() as server:
        msg = DDEMessageBase(func_name='GetDatabase', params=[DELIM])
        assert server.send_message(msg)[0] == 'Tutorial', 'Must Use Tutorial DB'
        yield server
        thread_id = threading.get_ident()
        logger.warning(f'AFTER YEILD {thread_id}')
    thread_id = threading.get_ident()
    logger.warning(f'OUSIDE CONTEXT {thread_id}')


@pytest.fixture(scope='function')
def dde_server() -> Generator[PyCmcDDEServer, None, None]:
    thread_id = threading.get_ident()
    logger.warning(f'DDEServer fixture running in thread {thread_id}')
    inititialized = False
    with PyCmcDDEServer() as server:
        try:
            # inititialized = initialise_com_multithreaded()
            msg = DDEMessageBase(func_name='GetDatabase', params=[DELIM])
            assert server.send_message(msg)[0] == 'Tutorial', 'Must Use Tutorial DB'
            yield server

        finally:
            if inititialized:
                comtypes.CoUninitialize()


@contextlib.contextmanager
def temp_contact(server: PyCmcDDEServer):
    item_name = TEST_ITEM_NAME
    category = 'Contact'
    try:
        server.view_reset(category)
        assert server.item_add(category, item_name, DDETopic.GET) is True
        yield server

    finally:
        logger.info('Cleaning up temp contact')
        assert server.item_delete(category, item_name, DDETopic.GET) is True
