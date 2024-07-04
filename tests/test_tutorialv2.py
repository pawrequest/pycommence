import contextlib

import pytest
from loguru import logger

from .conftest import NEW_DICT, NEW_KEY, UpdateDict
from pycommence.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.pycommence_v2 import PyCommence
from pycommence.pycmc_types import Connection2


def test_pycmc(pyc_contact_prm):
    assert pyc_contact_prm
    for rec in pyc_contact_prm.csr().rows(3):
        print(rec)


@contextlib.contextmanager
def temp_contact(pycmc: PyCommence):
    try:
        pycmc.csr().create_row_by_pkg(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        for row_id in pycmc.csr().pk_to_row_ids(NEW_KEY):
            logger.info('Deleted temp record')
            pycmc.csr().delete_row_by_id(row_id)


def test_temp_contact(pyc_contact_prm):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.csr().read_one_row_pk(NEW_KEY)
    with temp_contact(pyc_contact_prm):
        res = pyc_contact_prm.csr().read_one_row_pk(NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.csr().read_one_row_pk(NEW_KEY)


def test_get_records(pyc_contact_prm):
    res = list(pyc_contact_prm.csr().rows(2))
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pyc_contact_prm: PyCommence):
    with temp_contact(pyc_contact_prm):
        res = pyc_contact_prm.csr().read_one_row_pk(NEW_KEY)
        assert isinstance(res, dict)
        assert res['Notes'] == 'Some Notes'


def test_edit_record(pyc_contact_prm: PyCommence):
    with temp_contact(pyc_contact_prm):
        csr = pyc_contact_prm.csr()
        original = csr.read_one_row_pk(NEW_KEY)

        csr.update_row_by_pk(pk=NEW_KEY, update_pkg=UpdateDict)
        edited = csr.read_one_row_pk(NEW_KEY)
        for k, v in UpdateDict.items():
            assert edited[k] == v

        csr.update_row_by_pk(pk=NEW_KEY, update_pkg=original)
        reverted = csr.read_one_row_pk(NEW_KEY)
        assert reverted == original


def test_add_record(pyc_contact_prm: PyCommence):
    csr = pyc_contact_prm.csr()
    row_count1 = csr.row_count
    with temp_contact(pyc_contact_prm):
        pyc_contact_prm.refresh_csr(csr)
        row_count2 = pyc_contact_prm.csr().row_count
        assert row_count2 == row_count1 + 1

        res = pyc_contact_prm.csr().read_one_row_pk(NEW_KEY)
        for k, v in NEW_DICT.items():
            assert res[k] == v

    pyc_contact_prm.refresh_csr(csr)
    row_count3 = pyc_contact_prm.csr().row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pyc_contact_prm: PyCommence):
    with pytest.raises(PyCommenceExistsError):
        with temp_contact(pyc_contact_prm):
            pyc_contact_prm.csr().create_row_by_pkg(create_pkg=NEW_DICT)


def test_multiple_csrs(pyc_contact_prm: PyCommence):
    assert pyc_contact_prm
    pyc_contact_prm.set_csr(csrname='Account')
    assert pyc_contact_prm.csr(csrname='Account').category == 'Account'
    [print(pyc_contact_prm.csr(key).row_count, f'{key} records') for key in pyc_contact_prm.csrs.keys()]


def test_add_related(pyc_contact_prm:PyCommence):
    connection = Connection2(
        name='Relates To',
        category='Account',
        column='customerNumber',
    )
    allcols = pyc_contact_prm.csr().headers
    col_count = pyc_contact_prm.csr().column_count
    pyc_contact_prm.csr().add_related_column(connection)
    assert pyc_contact_prm.csr().column_count == col_count + 1