from typing import ClassVar

from pycommence.meta.meta import CommenceRecord, CommenceTable, get_table_type
from pycommence.rows import RowData2


def test_1(pycmc):

    row_data: RowData2 = pycmc.read_row2(pk='Bezos.Jeff')
    table_model = get_table_type(row_data.category)
    contact = CommenceRecord.from_dict(table_name='Contact', data=row_data.data)
    ...


