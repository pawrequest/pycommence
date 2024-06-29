import contextlib

import pytest

from .conftest import JEFF_EDITED_DICT, JEFF_EDITED_KEY, JEFF_KEY, UPDATE_PKG_1
from .. import PyCommenceExistsError, PyCommenceNotFoundError


def test_pycmc(pyc_contact_prm):
    assert pyc_contact_prm


@contextlib.contextmanager
def temp_geoff(pycmc):
    """Temporarily add JEFF_EDITED_DICT to Contact table. Remove after use."""
    try:
        pycmc.add_record(pk_val=JEFF_EDITED_KEY, row_dict=JEFF_EDITED_DICT)
        yield
    finally:
        pycmc.delete_record(pk_val=JEFF_EDITED_KEY)


def test_temp_geoff(pyc_contact_prm):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.one_record(JEFF_EDITED_KEY)
    with temp_geoff(pyc_contact_prm):
        res = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        assert res == JEFF_EDITED_DICT
    with pytest.raises(PyCommenceNotFoundError):
        pyc_contact_prm.one_record(JEFF_EDITED_KEY)


def test_get_records(pyc_contact_prm):
    res = pyc_contact_prm.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pyc_contact_prm):
    res = pyc_contact_prm.one_record(JEFF_KEY)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Jeff'


def test_edit_record(pyc_contact_prm):
    with temp_geoff(pyc_contact_prm):
        original = pyc_contact_prm.one_record(JEFF_EDITED_KEY)

        pyc_contact_prm.edit_record(pk_val=JEFF_EDITED_KEY, row_dict=UPDATE_PKG_1)
        edited = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert edited[k] == v

        pyc_contact_prm.edit_record(pk_val=JEFF_EDITED_KEY, row_dict=original)
        reverted = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        assert reverted == original


def test_add_record(pyc_contact_prm):
    csr = pyc_contact_prm.get_csr()
    row_count1 = csr.row_count
    with temp_geoff(pyc_contact_prm):
        row_count2 = csr.row_count
        assert row_count2 == row_count1 + 1

        res = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        assert len(res) == 61  # 61 fields in Contact
        for k, v in JEFF_EDITED_DICT.items():
            assert res[k] == v

    csr2 = pyc_contact_prm.get_csr()
    row_count3 = csr2.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pyc_contact_prm):
    with temp_geoff(pyc_contact_prm):
        with pytest.raises(PyCommenceExistsError):
            pyc_contact_prm.add_record(pk_val=JEFF_EDITED_KEY, row_dict=JEFF_EDITED_DICT)


def test_add_replace(pyc_contact_prm):
    with temp_geoff(pyc_contact_prm):
        pyc_contact_prm.add_record(pk_val=JEFF_EDITED_KEY, row_dict=UPDATE_PKG_1, existing='replace')
        res = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v


def test_add_update(pyc_contact_prm):
    with temp_geoff(pyc_contact_prm):
        pyc_contact_prm.add_record(pk_val=JEFF_EDITED_KEY, row_dict=UPDATE_PKG_1, existing='update')
        res = pyc_contact_prm.one_record(JEFF_EDITED_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert res[k] == v
