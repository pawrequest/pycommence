import contextlib

import pytest
from loguru import logger

from .conftest import NEW_DICT, NEW_KEY, UPDATE_DICT
from pycommence.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.pycommence_v2 import PyCommence


def test_pycmc(pycmc):
    assert pycmc


@contextlib.contextmanager
def temp_contact(pycmc):
    try:
        pycmc.add_record(pk_val=NEW_KEY, row_dict=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        pycmc.delete_record(pk_val=NEW_KEY, none_found='ignore')
        logger.info('Deleted temp record')


def test_temp_contact(pycmc):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.one_record(NEW_KEY)
    with temp_contact(pycmc):
        res = pycmc.one_record(NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.one_record(NEW_KEY)


def test_get_records(pycmc):
    res = pycmc.rows()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_gen_records(pycmc: PyCommence):
    for rec in pycmc.generate_records():
        print(rec)


def test_get_one_record(pycmc):
    with temp_contact(pycmc):
        res = pycmc.one_record(NEW_KEY)
        assert isinstance(res, dict)
        assert res['Notes'] == 'Some Notes'


def test_edit_record(pycmc):
    with temp_contact(pycmc):
        original = pycmc.one_record(NEW_KEY)

        pycmc.edit_record(pk_val=NEW_KEY, row_dict=UPDATE_DICT)
        edited = pycmc.one_record(NEW_KEY)
        for k, v in UPDATE_DICT.items():
            assert edited[k] == v

        pycmc.edit_record(pk_val=NEW_KEY, row_dict=original)
        reverted = pycmc.one_record(NEW_KEY)
        assert reverted == original


def test_add_record(pycmc):
    csr = pycmc.csr()
    row_count1 = csr.row_count
    with temp_contact(pycmc):
        # row_count2 = csr.row_count
        row_count2 = pycmc.csr().row_count
        assert row_count2 == row_count1 + 1

        res = pycmc.one_record(NEW_KEY)
        for k, v in NEW_DICT.items():
            assert res[k] == v

    csr2 = pycmc.csr()
    row_count3 = csr2.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc):
    with temp_contact(pycmc):
        with pytest.raises(PyCommenceExistsError):
            pycmc.add_record(pk_val=NEW_KEY, row_dict=NEW_DICT)


def test_multiple_csrs(pycmc: PyCommence):
    assert pycmc
    pycmc.set_csr(csrname='Account')
    assert pycmc.csr(csrname='Account').name == 'Account'
    [print(len(pycmc.records(csrname=key)), f'{key} records') for key in pycmc.csrs.keys()]
