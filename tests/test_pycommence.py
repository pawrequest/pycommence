import contextlib

import pytest

from pycommence.cursor import get_csr
from .conftest import GEOFF_DICT, GEOFF_KEY, JEFF_KEY, UPDATE_PKG_1
from pycommence.pycmc_types import CmcError
from pycommence import PyCommence


@pytest.fixture
def pycmc():
    """Get a Contact handler. Guarded against accidental use in non-Tutorial DB.
    in actual use we would likely use `Pycommence.from_table_name('Contact')` instead."""
    csr = get_csr('Contact')
    if not csr.db_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    yield PyCommence(csr=csr)


def test_pycmc(pycmc):
    assert isinstance(pycmc, PyCommence)


@contextlib.contextmanager
def temp_geoff(pycmc: PyCommence):
    """Temporarily add GEOFF_DICT to Contact table. Remove after use."""
    try:
        pycmc.add_record(pk_val=GEOFF_KEY, package=GEOFF_DICT)
        yield
    finally:
        pycmc.delete_record(pk_val=GEOFF_KEY)


def test_temp_geoff(pycmc):
    """Test add_record and delete_record."""
    with pytest.raises(CmcError):
        pycmc.one_record(GEOFF_KEY)
    with temp_geoff(pycmc):
        res = pycmc.one_record(GEOFF_KEY)
        assert res == GEOFF_DICT
    with pytest.raises(CmcError):
        pycmc.one_record(GEOFF_KEY)


def test_get_records(pycmc: PyCommence):
    res = pycmc.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pycmc: PyCommence):
    res = pycmc.one_record(JEFF_KEY)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Jeff'


def test_get_records_by_field(pycmc: PyCommence):
    res = pycmc.records_by_field('firstName', 'Jeff')
    assert isinstance(res, list)
    assert isinstance(res[0], dict)
    assert res[0]['firstName'] == 'Jeff'


def test_edit_record(pycmc: PyCommence):
    with temp_geoff(pycmc):
        original = pycmc.one_record(GEOFF_KEY)

        pycmc.edit_record(pk_val=GEOFF_KEY, package=UPDATE_PKG_1)
        edited = pycmc.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert edited[k] == v

        pycmc.edit_record(pk_val=GEOFF_KEY, package=original)
        reverted = pycmc.one_record(GEOFF_KEY)
        assert reverted == original


def test_add_record(pycmc: PyCommence):
    row_count1 = pycmc.csr.row_count
    with temp_geoff(pycmc):
        row_count2 = pycmc.csr.row_count
        assert row_count2 == row_count1 + 1

        handler2 = PyCommence.from_table_name('Contact')
        res = handler2.one_record(GEOFF_KEY)
        assert len(res) == 61  # 61 fields in Contact
        for k, v in GEOFF_DICT.items():
            assert res[k] == v

    row_count3 = pycmc.csr.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc: PyCommence):
    with temp_geoff(pycmc):
        with pytest.raises(CmcError):
            pycmc.add_record(pk_val=GEOFF_KEY, package=GEOFF_DICT)


def test_add_replace(pycmc: PyCommence):
    with temp_geoff(pycmc):
        pycmc.add_record(pk_val=GEOFF_KEY, package=UPDATE_PKG_1, existing='replace')
        res = pycmc.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v


def test_add_update(pycmc: PyCommence):
    with temp_geoff(pycmc):
        pycmc.add_record(pk_val=GEOFF_KEY, package=UPDATE_PKG_1, existing='update')
        res = pycmc.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v
