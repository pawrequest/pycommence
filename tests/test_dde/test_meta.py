from pycommence import PyCommence
from pycommence.core.meta import generate_table_pydantic_model, get_table_type_generate
from pycommence.core.pagination import Pagination
from pycommence.core.type_manipulations import make_partial
from pycommence.dde import DDETopic


def test_generate_table(test_client):
    category = 'Contact'
    conv = test_client.conversation(DDETopic.VIEW)
    fields_defs = conv.category_field_definitions(category)
    clz = generate_table_pydantic_model(
        field_def_dict=fields_defs,
        name=category,
        category=category,
    )
    suffix = 'Add'
    prefix = ''
    clz = make_partial(clz, prefix=prefix, suffix=suffix)

    conv.view_reset(category)
    csr = test_client.cursor(category)
    data = csr.read_rows(Pagination(limit=3))
    row = next(data)

    obj = clz.model_validate(row.data)
    assert obj.__class__.__name__ == prefix + category + suffix
    ...


def test_2(test_client: PyCommence):
    generated_table = get_table_type_generate('Contact', test_client)
    contact = test_client.item_read_dde('Contact', 'Musk.Elon')
    model = generated_table.model_validate(contact)
    assert model.__class__.__name__ == 'Contact'
