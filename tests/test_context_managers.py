from pycommence.pycmc_types import CursorType
from pycommence.pycommence_v2 import pycommence_context


def test_pycmc_context():
    with pycommence_context(csrname='Contact') as pycmc2:
        csr = pycmc2.csr()
        print(csr.row_count)


