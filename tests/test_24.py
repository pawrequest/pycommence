from pycommence.pycmc_types import CursorType
from pycommence.pycommence_v2 import pycommence_context


def test_24():
    with pycommence_context(csrname='Customer') as pycmc2:
        csr = pycmc2.csr()
        # rowset = csr.get_query_row_set()
        print(csr.row_count)


def test_24_view():
    with pycommence_context(csrname='Hires Outbound - Paul', mode=CursorType.VIEW) as pycmc2:
        csr = pycmc2.csr()
        # rowset = csr.get_query_row_set()
        print(csr.row_count)
