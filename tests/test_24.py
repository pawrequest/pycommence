from amherst.back.backend_pycommence import pycommence_context2
from amherst.models.commence_adaptors import AmherstTableName


def test_24():
    with pycommence_context2(csrname=AmherstTableName.Customer) as pycmc2:
        csr = pycmc2.csr().cursor_wrapper
        rowset = csr.get_query_row_set()
        print(rowset.row_count)
