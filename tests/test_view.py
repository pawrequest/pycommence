import pytest

from pycommence.pycmc_types import CursorType
from pycommence.pycommence import PyCommence


@pytest.fixture
def pycmc_view():
    pycmc = PyCommence.with_csr('Contact List', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def test_view(pycmc_view):
    rows = pycmc_view.read_rows()
    print(len(list(rows)), 'records')
