import pytest

from pycommence.pycmc_types import CursorType
from pycommence.pycommence_v2 import PyCommence


@pytest.fixture
def pycmc():
    pycmc = PyCommence.with_csr('Contact List', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def test_view(pycmc):
    print(len(list(pycmc.read_rows())), 'records')

