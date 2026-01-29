import pytest

from pycommence.dde.msgs import get
from pycommence.dde.dde_errors import PyCmcDDEError

TESTCOUNT = 5


def test_get_field_count_invalid_category(pycmc_client):
    msg = get.field_count('InvalidCategory')
    with pytest.raises(PyCmcDDEError) as e:
        pycmc_client.send_dde_message(msg)
    res = r"PyCmcDDEError('Unsupported clipboard format')"
    ...


def test_get_item_count_empty_category(pycmc_client):
    msg = get.item_count('')
    with pytest.raises(PyCmcDDEError) as e:
        pycmc_client.send_dde_message(msg)
    ...


def test_get_field_invalid_item(pycmc_client):
    msg = get.field('Contact', '99999', 'Name')
    with pytest.raises(PyCmcDDEError) as e:
        pycmc_client.send_dde_message(msg)
    ...


def test_get_fields_invalid_fields_list(pycmc_client):
    msg = get.fields('Contact', 'Musk.Elon', ['invalidField1', 'invalidField2'])
    with pytest.raises(PyCmcDDEError) as e:
        pycmc_client.send_dde_message(msg)
    ...


def test_get_category_definition_nonexistent(pycmc_client):
    msg = get.category_definition('NonExistentCategory')
    with pytest.raises(PyCmcDDEError) as e:
        pycmc_client.send_dde_message(msg)
    ...
