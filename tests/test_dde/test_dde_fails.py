import pytest

from pycommence.dde.msgs.get import (
    get_category_definition,
    get_field,
    get_field_count,
    get_fields,
    get_item_count,
)
from pycommence.dde.dde_errors import PyCmcDDEError

TESTCOUNT = 5


def test_get_field_count_invalid_category(dde_server):
    msg = get_field_count('InvalidCategory')
    with pytest.raises(PyCmcDDEError) as e:
        dde_server.send_message(msg)
    res = r"PyCmcDDEError('Unsupported clipboard format')"
    ...


def test_get_item_count_empty_category(dde_server):
    msg = get_item_count('')
    with pytest.raises(PyCmcDDEError) as e:
        dde_server.send_message(msg)
    ...


def test_get_field_invalid_item(dde_server):
    msg = get_field('Contact', '99999', 'Name')
    with pytest.raises(PyCmcDDEError) as e:
        dde_server.send_message(msg)
    ...


def test_get_fields_invalid_fields_list(dde_server):
    msg = get_fields('Contact', 'Musk.Elon', ['invalidField1', 'invalidField2'])
    with pytest.raises(PyCmcDDEError) as e:
        dde_server.send_message(msg)
    ...


def test_get_category_definition_nonexistent(dde_server):
    msg = get_category_definition('NonExistentCategory')
    with pytest.raises(PyCmcDDEError) as e:
        dde_server.send_message(msg)
    ...
