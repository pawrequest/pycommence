from typing import ClassVar

import pytest

from pycommence import pycommence_context
from pycommence.meta.meta import CommenceTable
from pycommence.pycommence import PyCommence


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
    with pycommence_context() as pycmc:
        return pycmc


class Contact(CommenceTable):
    category: ClassVar[str] = "Contact"
    pk_key: ClassVar[str] = "contactKey"


class Account(CommenceTable):
    category: ClassVar[str] = "Account"
    pk_key: ClassVar[str] = "accountKey"
