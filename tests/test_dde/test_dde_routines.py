from sample_data import CONTACT_FIELD_NAMES
from pycommence.dde import routines
from pycommence.core.fields import CmcDefsDict, CmcFieldDefinition

TESTCOUNT = 5

def test_rout(dde_server):
    res:CmcDefsDict = routines.fetch_category_field_definitions_dir('Contact', dde_server)
    name_field = res.name_field()
    ...


def test_fetch_field_names(dde_server):
    category = 'Contact'
    field_names = routines.fetch_field_names(category, dde_server)
    assert field_names == CONTACT_FIELD_NAMES


def test_fetch_field_definition(dde_server):
    category = 'Contact'
    field_name = 'firstName'
    field_definition = routines.fetch_field_definition(category, field_name, dde_server)
    assert isinstance(field_definition, CmcFieldDefinition)
    assert field_definition.type.py_type is str


def test_fetch_category_field_definitions_dir(dde_server):
    category = 'Contact'
    field_definitions = routines.fetch_category_field_definitions_dir(category, dde_server)
    assert isinstance(field_definitions, CmcDefsDict)
    assert 'Account' in field_definitions
    assert 'busCity' in field_definitions


def test_get_item_routine(dde_server):
    category = 'Contact'
    pk_value = 'Bezos.Jeff'
    result = routines.get_item_dict(category, pk_value, dde_server)
    assert isinstance(result, dict)
    assert result['firstName'] == 'Jeff'
