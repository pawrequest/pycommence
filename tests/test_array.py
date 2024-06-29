import pytest

from pycommence import FilterArray
from pycommence.bench.pycommence_v1 import PyCommenceV1
from pycommence.pycmc_types import CmcFilter


@pytest.fixture
def fil1():
    return CmcFilter(
        cmc_col='Status',
        condition='Equal To',
        value='Booked In',
    )


@pytest.fixture
def pycmc_radios_hire():
    pycmc = PyCommenceV1.with_csr('Hire')
    assert isinstance(pycmc, PyCommenceV1)
    return pycmc


@pytest.fixture
def fil_array(fil1):
    fil_array = FilterArray(filters={1: fil1})
    assert isinstance(fil_array, FilterArray)
    assert fil_array.filters[1] == fil1
    return fil_array


def test_fiters(pycmc_radios_hire, fil_array):
    count = pycmc_radios_hire.csrs['Hire'].row_count
    with pycmc_radios_hire.csrs['Hire'].temporary_filter_by_array(fil_array):
        c2 = pycmc_radios_hire.csrs['Hire'].row_count
        assert c2 < count
        ...


def test_records(fil_array, pycmc_radios_hire):
    print('Filter:', fil_array)
    records = pycmc_radios_hire.records_by_array('Hire', fil_array)
    print(len(records), 'records found.')
    [
        print(record['Name'], 'Status:', record['Status'], 'Send Date:', record['Send Out Date'])
        for record in records
    ]
    assert records
