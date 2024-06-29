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
