import contextlib

import pytest

from pycommence.api.csr_api import Csr, csr_context
from pycommence.api import csr_handler
from .conftest import GEOFF_DICT, GEOFF_KEY, JEFF_KEY, UPDATE_PKG_1


@pytest.fixture
def contact_handler():
    with csr_context("Contact") as csr:
        if not csr.db_name == 'Tutorial':
            raise ValueError("Expected Tutorial DB")
        yield csr_handler.CmcHandler(csr=csr)


@contextlib.contextmanager
def temp_geoff(con_handler: csr_handler.CmcHandler):
    try:
        con_handler.add_record(pk_val=GEOFF_KEY, package=GEOFF_DICT)
        yield
    finally:
        con_handler.csr.delete_record(pk_val=GEOFF_KEY)


def test_contact_handler(contact_handler):
    assert isinstance(contact_handler, csr_handler.CmcHandler)


def test_get_records(contact_handler: csr_handler.CmcHandler):
    res = contact_handler.records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(contact_handler: csr_handler.CmcHandler):
    res = contact_handler.one_record(JEFF_KEY)
    assert isinstance(res, dict)
    assert res['firstName'] == 'Jeff'


def test_get_records_by_field(contact_handler: csr_handler.CmcHandler):
    res = contact_handler.records_by_field('firstName', 'Jeff')
    assert isinstance(res, list)
    assert isinstance(res[0], dict)
    assert res[0]['firstName'] == 'Jeff'


def test_edit_record(contact_handler: csr_handler.CmcHandler):
    with temp_geoff(contact_handler):
        original = contact_handler.one_record(GEOFF_KEY)
        contact_handler.edit_record(pk_val=GEOFF_KEY, package=UPDATE_PKG_1)
        edited = contact_handler.one_record(GEOFF_KEY)
        for k, v in UPDATE_PKG_1.items():
            assert edited[k] == v
        contact_handler.edit_record(pk_val=GEOFF_KEY, package=original)
        reverted = contact_handler.one_record(GEOFF_KEY)
        assert reverted == original


def test_add_record(contact_handler: csr_handler.CmcHandler):
    row_count1 = contact_handler.csr.row_count
    with temp_geoff(contact_handler):
        row_count2 = contact_handler.csr.row_count
        assert row_count2 == row_count1 + 1

        with csr_context('Contact') as cs2:
            res = cs2.one_record(GEOFF_KEY)
        assert len(res) == 61  # 61 fields in Contact
        for k, v in GEOFF_DICT.items():
            assert res[k] == v

    row_count3 = contact_handler.csr.row_count
    assert row_count3 == row_count1

