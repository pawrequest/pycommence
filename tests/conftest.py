from typing import ClassVar, Generator

import pytest

from pycommence.dde_generators.dde_msg import DDEMessage
from pycommence.dde_generators.dde_server import DDEServer
from pycommence.dde_generators.dde_server_pycmc import CommenceDDEServer
from pycommence.meta.meta import CommenceTableGenerated
from pycommence.meta.pycmc_fields import DELIM
from pycommence.pycommence import PyCommence
from pycommence.wrapper.conversation_wrapper import DDETopic


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
    category: ClassVar[str] = "Contact"
    pk_key: ClassVar[str] = "contactKey"


class Account(CommenceTableGenerated):
    category: ClassVar[str] = "Account"
    pk_key: ClassVar[str] = "accountKey"


@pytest.fixture(scope='session')
def dde_server() -> Generator[CommenceDDEServer]:
    with CommenceDDEServer(DDETopic.GET) as server:
        msg = DDEMessage(func_name='GetDatabase', params=[DELIM])
        assert server.send_message(msg)[0] == 'Tutorial', "Must Use Tutorial DB"
        yield server
