import pytest

from pycommence import pycommence_context
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
