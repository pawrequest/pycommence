import pytest

from pycommence.pycmc_types import CursorType
from pycommence.pycommence_v2 import PyCommence


@pytest.fixture
def pycmc():
    pycmc = PyCommence.with_csr('paul hires', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.delivery_contact_name == 'Radios':
        raise ValueError('Expected Radios DB')
    return pycmc


def test_view(pycmc):
    print(len(pycmc._read_rows()), 'records')
