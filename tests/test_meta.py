from conftest import get_pycmc
from pycommence.dde_generators.pycmc_dde.routines import fetch_category_field_definitions
from pycommence.meta.meta import generate_table_class_from_field_defs
from pycommence.meta.pycmc_fields import CmcDefsDict
from pycommence.pagination import Pagination


def test_generate_table():
    category = 'Address'
    fields_defs: CmcDefsDict = fetch_category_field_definitions(category=category)
    clz = generate_table_class_from_field_defs(
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
