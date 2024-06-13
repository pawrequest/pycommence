import contextlib

import pytest

from pycommence.cursor import get_csr
from .conftest import GEOFF_DICT, GEOFF_KEY, JEFF_KEY, RICHARD_KEY, UPDATE_PKG_1
from pycommence.pycmc_types import (
    CmcError,
    FilterArray,
    FilterConditionType,
)
from pycommence import PyCommence, pycmc_types


@pytest.fixture
def pycmc_contact():
    """Get a Contact handler. Guarded against accidental use in non-Tutorial DB.
    in actual use we would likely use `Pycommence.from_table_name('Contact')` instead."""
    csr = get_csr('Contact')
    if not csr.db_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    yield PyCommence(csr=csr)


@pytest.fixture
def pycmc_radios_hire():
    csr = get_csr('Hire')
    yield PyCommence(csr=csr)


@pytest.fixture
def pycmc_account():
    csr = get_csr('Account')
    if not csr.db_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    yield PyCommence(csr=csr)


def test_pycmc(pycmc_contact):
    assert isinstance(pycmc_contact, PyCommence)


@contextlib.contextmanager
def temp_geoff(pycmc: PyCommence):
    """Temporarily add GEOFF_DICT to Contact table. Remove after use."""
    try:
        pycmc.add_record(pk_val=GEOFF_KEY, row_dict=GEOFF_DICT)
        yield
    finally:
        pycmc.delete_record(pk_val=GEOFF_KEY)


def test_temp_geoff(pycmc_contact):
    """Test add_record and delete_record."""
    with pytest.raises(CmcError):
        pycmc_contact.one_record(GEOFF_KEY)
    with temp_geoff(pycmc_contact):
        res = pycmc_contact.one_record(GEOFF_KEY)
        assert res == GEOFF_DICT
    with pytest.raises(CmcError):
        pycmc_contact.one_record(GEOFF_KEY)


def test_get_records(pycmc_contact: PyCommence):
    res = pycmc_contact.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pycmc_contact: PyCommence):
    res = pycmc_contact.one_record(JEFF_KEY)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Jeff'


def test_get_records_by_field(pycmc_contact: PyCommence):
    res = pycmc_contact.records_by_field('firstName', 'Jeff')
    assert isinstance(res, list)
    assert isinstance(res[0], dict)
    assert res[0]['firstName'] == 'Jeff'


def test_edit_record(pycmc_contact: PyCommence):
    with temp_geoff(pycmc_contact):
        original = pycmc_contact.one_record(GEOFF_KEY)

        pycmc_contact.edit_record(pk_val=GEOFF_KEY, row_dict=UPDATE_PKG_1)
        edited = pycmc_contact.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert edited[k] == v

        pycmc_contact.edit_record(pk_val=GEOFF_KEY, row_dict=original)
        reverted = pycmc_contact.one_record(GEOFF_KEY)
        assert reverted == original


def test_edit_record2(pycmc_contact: PyCommence):
    pycmc_contact.edit_record(pk_val=RICHARD_KEY, row_dict=UPDATE_PKG_1)
    edited = pycmc_contact.one_record(RICHARD_KEY)
    for k, v in UPDATE_PKG_1.items():
        assert edited[k] == v


def test_add_record(pycmc_contact: PyCommence):
    row_count1 = pycmc_contact.csr.row_count
    with temp_geoff(pycmc_contact):
        row_count2 = pycmc_contact.csr.row_count
        assert row_count2 == row_count1 + 1

        handler2 = PyCommence.from_table_name('Contact')
        res = handler2.one_record(GEOFF_KEY)
        assert len(res) == 61  # 61 fields in Contact
        for k, v in GEOFF_DICT.items():
            assert res[k] == v

    row_count3 = pycmc_contact.csr.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc_contact: PyCommence):
    with temp_geoff(pycmc_contact):
        with pytest.raises(CmcError):
            pycmc_contact.add_record(pk_val=GEOFF_KEY, row_dict=GEOFF_DICT)


def test_add_replace(pycmc_contact: PyCommence):
    with temp_geoff(pycmc_contact):
        pycmc_contact.add_record(pk_val=GEOFF_KEY, row_dict=UPDATE_PKG_1, existing='replace')
        res = pycmc_contact.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v


def test_add_update(pycmc_contact: PyCommence):
    with temp_geoff(pycmc_contact):
        pycmc_contact.add_record(pk_val=GEOFF_KEY, row_dict=UPDATE_PKG_1, existing='update')
        res = pycmc_contact.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v


@pytest.fixture
def fil1():
    return pycmc_types.CmcFilter(
        cmc_col='Status',
        condition='Equal To',
        value='Booked In',
    )


@pytest.fixture
def fil_array(fil1):
    fil_array = FilterArray(filters={1: fil1})
    assert isinstance(fil_array, FilterArray)
    assert fil_array.filters[1] == fil1
    return fil_array


def test_fiters(pycmc_radios_hire, fil_array):
    count = pycmc_radios_hire.csr.row_count
    with pycmc_radios_hire.csr.temporary_filter_by_array(fil_array):
        c2 = pycmc_radios_hire.csr.row_count
        assert c2 > count
        ...
