from pycommence.api import Csr

"""USE TUTORIAL DB"""


def test_hire_csr(contact_csr):
    assert isinstance(contact_csr, Csr)


def test_get_records(contact_csr: Csr):
    res = contact_csr.get_records()
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_add_record(contact_csr: Csr):
    res = contact_csr.add_record(record_name='test_contact', package={'firstName': 'fn test'})
    assert res


def test_get_contacts(contact_csr: Csr):
    res = contact_csr.get_records()
    ...
