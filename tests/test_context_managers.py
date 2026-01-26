from pycommence.pycmc_types import CursorType
from pycommence import pycommence_context


def test_pycmc_context():
    with pycommence_context('Contact') as pycmc2:
        csr = pycmc2.csr()
        print(csr.row_count)


