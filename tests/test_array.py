import pytest

from pycommence.filters import FieldFilter, FilterArray
from pycommence.pycommence_v2 import PyCommence


@pytest.fixture
def fil1():
    return FieldFilter(
        column='Status',
        condition='Equal To',
        value='Booked In',
    )


@pytest.fixture
def pycmc_radios_hire():
    pycmc = PyCommence.with_csr('Hire')
    assert isinstance(pycmc, PyCommence)
    return pycmc


@pytest.fixture
def fil_array(fil1):
    fil_array = FilterArray(filters={1: fil1})
    assert isinstance(fil_array, FilterArray)
    assert fil_array.filters[1] == fil1
    return fil_array


def test_fiters(pycmc_radios_hire, fil_array):
    count = pycmc_radios_hire.csrs['Hire'].row_count
    with pycmc_radios_hire.csrs['Hire'].temporary_filter(fil_array):
        c2 = pycmc_radios_hire.csrs['Hire'].row_count
        assert c2 < count
        ...


def test_records(fil_array, pycmc_radios_hire):
    print('Filter:', fil_array)
    records = list(pycmc_radios_hire.csr().read_rows_filtered(fil_array))
    assert records


def test_cols(pycmc_radios_hire):
    cols = pycmc_radios_hire.csr().headers
    assert cols
    print(cols)
