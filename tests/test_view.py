import pytest

from pycommence.pyc2 import PyCommence
from pycommence.wrapper.enums_cmc import CursorType


@pytest.fixture
def pycmc():
    pycmc = PyCommence.with_csr('paul hires', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.name == 'Radios':
        raise ValueError('Expected Radios DB')
    return pycmc


def test_view(pycmc):
    print(len(pycmc.records()), 'records')
#
# @pytest.fixture
# def pycmc():
#     pycmc = PyCommence.with_csr('newView', mode=CursorType.VIEW)
#     if not pycmc.cmc_wrapper.name == 'Tutorial':
#         raise ValueError('Expected Tutorial DB')
#     return pycmc
#
#
# def test_view(pycmc):
#     assert pycmc.cmc_wrapper.name == 'Tutorial'
#     print(len(pycmc.records()), 'records')
