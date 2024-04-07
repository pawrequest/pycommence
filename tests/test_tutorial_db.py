import pycommence.api
from pycommence.api import Csr, csr_context

"""USE TUTORIAL DB"""


def test_contact_csr(contact_csr):
    assert isinstance(contact_csr, Csr)


def test_get_records(contact_csr: Csr):
    res = contact_csr.get_records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_clear_filter(contact_csr: Csr):
    row_count1 = contact_csr.row_count
    contact_csr.filter_by_pk('Bezos.Jeff')
    row_count2 = contact_csr.row_count
    assert row_count2 == 1
    contact_csr.clear_filter()
    assert contact_csr.row_count == row_count1

def test_add_record(contact_csr: Csr):
    row_count1 = contact_csr.row_count
    contact_csr.add_record(pk_val='Col0 Val', package={'firstName': 'test2'})
    row_count2 = contact_csr.row_count
    assert row_count2 == row_count1 + 1

    with pycommence.api.csr_context('Contact') as cs2:
        res = cs2.records_by_field(field_name='firstName', value='test2')
    assert res
    assert res[0]['firstName'] == 'test2'


def test_tst():
    with csr_context("cat") as csr:
        recs = csr.get_records()
        ...
