import contextlib

import pytest
from loguru import logger

from .conftest import NEW_DICT, NEW_KEY, UpdateDict
from pycommence.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.pycommence_v2 import PyCommence


def test_pycmc(pyc_contact_prm):
    assert pyc_contact_prm
    print(len(pyc_contact_prm.records()), 'records')


@contextlib.contextmanager
def temp_contact(pycmc):
    try:
        pycmc.add_record(pk_val=NEW_KEY, row_dict=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        pycmc.delete_record(pk_val=NEW_KEY, none_found='ignore')
        logger.info('Deleted temp record')


def test_temp_contact(pyc_contact_prm):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.one_record(NEW_KEY)
    with temp_contact(pyc_contact_prm):
        res = pyc_contact_prm.one_record(NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.one_record(NEW_KEY)


def test_get_records(pyc_contact_prm):
    res = pyc_contact_prm.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_gen_records(pyc_contact_prm: PyCommence):
    for rec in pyc_contact_prm.generate_records():
        print(rec)


def test_get_one_record(pyc_contact_prm):
    with temp_contact(pyc_contact_prm):
        res = pyc_contact_prm.one_record(NEW_KEY)
        assert isinstance(res, dict)
        assert res['Notes'] == 'Some Notes'


def test_edit_record(pyc_contact_prm):
    with temp_contact(pyc_contact_prm):
        original = pyc_contact_prm.one_record(NEW_KEY)

        pyc_contact_prm.edit_record(pk_val=NEW_KEY, row_dict=UpdateDict)
        edited = pyc_contact_prm.one_record(NEW_KEY)
        for k, v in UpdateDict.items():
            assert edited[k] == v

        pyc_contact_prm.edit_record(pk_val=NEW_KEY, row_dict=original)
        reverted = pyc_contact_prm.one_record(NEW_KEY)
        assert reverted == original


def test_add_record(pyc_contact_prm):
    csr = pyc_contact_prm.get_csr()
    row_count1 = csr.row_count
    with temp_contact(pyc_contact_prm):
        # row_count2 = csr.row_count
        row_count2 = pyc_contact_prm.get_csr().row_count
        assert row_count2 == row_count1 + 1

        res = pyc_contact_prm.one_record(NEW_KEY)
        for k, v in NEW_DICT.items():
            assert res[k] == v

    csr2 = pyc_contact_prm.get_csr()
    row_count3 = csr2.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pyc_contact_prm):
    with temp_contact(pyc_contact_prm):
        with pytest.raises(PyCommenceExistsError):
            pyc_contact_prm.add_record(pk_val=NEW_KEY, row_dict=NEW_DICT)


def test_multiple_csrs(pyc_contact_prm: PyCommence):
    assert pyc_contact_prm
    pyc_contact_prm.set_csr(csrname='Account')
    assert pyc_contact_prm.get_csr(csrname='Account').name == 'Account'
    [print(len(pyc_contact_prm.records(csrname=key)), f'{key} records') for key in pyc_contact_prm.csrs.keys()]
