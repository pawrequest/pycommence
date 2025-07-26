from pycommence.bench.pycommence_v1 import PyCommenceV1
from pycommence.cursor import get_csr


def pyc_contact_old():
    csr = get_csr('Contact')
    if not csr.db_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return PyCommenceV1(csr=csr)
