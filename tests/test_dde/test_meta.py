from pycommence.core.meta import generate_table_pydantic_model
from pycommence.core.pagination import Pagination
from pycommence.dde import DDETopic


def test_generate_table(pycmc_client):
    category = 'Address'
    conv = pycmc_client.conversation(DDETopic.GET)
    fields_defs = conv.category_field_definitions(category)
    clz = generate_table_pydantic_model(
        field_def_dict=fields_defs,
        name=category,
        category=category,
    )

    csr = pycmc_client.cursor(category)
    data = csr.read_rows(Pagination(limit=3))
    row = next(data)

    obj = clz.model_validate(row.data)
    assert obj.__class__.__name__ == category
    ...
