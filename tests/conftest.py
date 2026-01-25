# @pytest.fixture(autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(1)
import pytest

from pycommence import pycommence_context
from pycommence.pycommence import PyCommence


@pytest.fixture(scope='function')
def pycmc_fxt():
    pycmc = PyCommence.with_csr('Contact')
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def get_new_pycmc(tblname: str | None = None):
    pycmc = PyCommence()
    if tblname:
        pycmc.set_csr(csrname=tblname)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def pyc_w_contact_csr():
    return get_new_pycmc('Contact')


@pytest.fixture(scope='function', params=[pyc_w_contact_csr])
# @pytest.fixture(scope='function', params=[pyc_w_contact_csr, pycmc_view_cursor])
def pycmc(request) -> PyCommence:
    param = request.param
    return param()


@pytest.fixture(scope='function')
def pycmc_no_csr() -> PyCommence:
    with pycommence_context() as pycmc:
        return pycmc

# __all__ = [
# ]
