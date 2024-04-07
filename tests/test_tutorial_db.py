import pytest

from pycommence.api import Csr, csr_context
from .conftest import GEOFF_DICT, GEOFF_KEY, JEFF_KEY, UPDATE_PKG_1


@pytest.fixture
def contact_csr():
    with csr_context("Contact") as csr:
        if not csr.db_name == 'Tutorial':
            raise ValueError("Expected Tutorial DB")
        yield csr


def test_contact_csr(contact_csr):
    assert isinstance(contact_csr, Csr)


def test_get_records(contact_csr: Csr):
    res = contact_csr.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_clear_filter(contact_csr: Csr):
    row_count1 = contact_csr.row_count
    contact_csr.filter_by_pk(JEFF_KEY)
    row_count2 = contact_csr.row_count
    assert row_count2 == 1
    contact_csr.clear_filter()
    assert contact_csr.row_count == row_count1


def test_add_record(contact_csr: Csr):
    contact_csr.delete_record(pk_val=GEOFF_KEY, empty='ignore')
    row_count1 = contact_csr.row_count
    contact_csr.add_record(pk_val=GEOFF_KEY, package=GEOFF_DICT)
    row_count2 = contact_csr.row_count
    assert row_count2 == row_count1 + 1

    with csr_context('Contact') as cs2:
        res = cs2.one_record(GEOFF_KEY)
    assert len(res) == 61  # 61 fields in Contact
    for k, v in GEOFF_DICT.items():
        assert res[k] == v


def test_edit_record(contact_csr: Csr):
    contact_csr.edit_record(pk_val=GEOFF_KEY, package=UPDATE_PKG_1)
    res = contact_csr.one_record(pk_val=GEOFF_KEY)
    for k, v in UPDATE_PKG_1.items():
        assert res[k] == v


def test_temp_filter(contact_csr: Csr):
    with contact_csr.temporary_filter_pk(JEFF_KEY):
        assert contact_csr.row_count == 1
    assert contact_csr.row_count > 1
