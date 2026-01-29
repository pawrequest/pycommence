from conftest import get_pycmc
from pycommence.core.meta import generate_table_pydantic_model
from pycommence.core.fields import CmcDefsDict
from pycommence.core.pagination import Pagination


def test_generate_table(dde_server):
    category = 'Address'
    fields_defs: CmcDefsDict = dde_server.fields_definition_dict(category)
    clz = generate_table_pydantic_model(
        field_def_dict=fields_defs,
        name=category,
        category=category,
    )

    p = get_pycmc(category)
    data = p.csr().read_rows(Pagination(limit=3))
    row = next(data)

    obj = clz.model_validate(row.data)
    assert obj.__class__.__name__ == category
    ...
