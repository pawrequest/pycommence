import pycommence.api
from pycommence.api import Csr

"""USE TUTORIAL DB"""


def test_contact_csr(contact_csr):
    assert isinstance(contact_csr, Csr)


def test_get_records(contact_csr: Csr):
    res = contact_csr.get_records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_add_record(contact_csr: Csr):
    res = contact_csr.add_record(col_0='moretest', package={'firstName': 'test2'})
    with pycommence.api.csr_context('Contact') as cs2:
        rec = cs2.records_by_field(field_name='contactKey', value='test_contact')
    assert rec
    assert rec[0]['firstName'] == 'fn test'


