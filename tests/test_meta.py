from typing import ClassVar

from pycommence.meta.meta import CommenceRecord2, CommenceTable, get_table_model
from pycommence.rows import RowData2


class Contact(CommenceTable):
    category: ClassVar[str] = "Contact"
    pk_key: ClassVar[str] = "contactKey"


def test_1(pycmc_fxt):
    row_data: RowData2 = pycmc_fxt.read_row2(pk='Bezos.Jeff')
    table_model = get_table_model(row_data.category)
    contact = CommenceRecord2(table=table_model, data=row_data.data)
    ...

