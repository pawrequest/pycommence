import pytest

from pycommence.dde import DDEMessageBase, DDETopic
from pycommence.dde.msgs import get

TESTCOUNT = 34 + 3


def test_msg(pycmc_client):
    msg = DDEMessageBase(func_name='GetFieldCount', params=['Contact'], topic=DDETopic.GET)
    res = pycmc_client.send_dde_message(msg)
    assert res == '45'


####

def test_clarify_item_names(pycmc_client):
    msg = get.clarify_item_names()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_active_view_info(pycmc_client):
    msg = get.active_view_info()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_caller_id(pycmc_client):
    msg = get.caller_id('Contact', '412-555-7890')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_category_count(pycmc_client):
    msg = get.category_count()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_category_definition(pycmc_client, timed):
    msg = get.category_definition('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_category_names(pycmc_client):
    msg = get.category_names()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_connection_count(pycmc_client):
    msg = get.connection_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_connection_names(pycmc_client):
    msg = get.connection_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_database(pycmc_client):
    msg = get.database()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_database_definition(pycmc_client):
    msg = get.database_definition()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_desktop_count(pycmc_client):
    msg = get.desktop_count()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_desktop_names(pycmc_client):
    msg = get.desktop_names()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_field(pycmc_client):
    msg = get.field('Contact', 'Musk.Elon', 'Name')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_fields(pycmc_client):
    msg = get.fields('Contact', 'Musk.Elon', ['firstName', 'lastName'])
    res = pycmc_client.send_dde_message(msg)
    assert res == ['Elon', 'Musk']


def test_get_field_count(pycmc_client):
    msg = get.field_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_field_definition(pycmc_client):
    msg = get.field_definition('Contact', 'firstName')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_field_names(pycmc_client):
    msg = get.field_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_field_to_file(pycmc_client):
    msg = get.field_to_file('Contact', 'Musk.Elon', 'Name', 'test.txt')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_form_count(pycmc_client):
    msg = get.form_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_form_names(pycmc_client):
    msg = get.form_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_image_field_count(pycmc_client):
    msg = get.image_field_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_names(pycmc_client):
    msg = get.image_field_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_to_file(pycmc_client):
    msg = get.image_field_to_file('Contact', '1', 'Photo', 'test.jpg')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_item_count(pycmc_client):
    msg = get.item_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_item_names(pycmc_client):
    msg = get.item_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_last_error(pycmc_client):
    msg = get.last_error()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_mark_item(pycmc_client):
    msg = get.mark_item('Contact', 'Musk.Elon')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_mark_active_item(pycmc_client):
    msg = get.mark_active_item()
    res = pycmc_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='Requires TAPI setup')
def test_get_phone_number(pycmc_client):
    msg = get.phone_number('412-555-7890')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_preference(pycmc_client):
    msg = get.preference('ME')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_reverse_name(pycmc_client):
    msg = get.reverse_name('John Doe')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_trigger_count(pycmc_client):
    msg = get.trigger_count()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_trigger_names(pycmc_client):
    msg = get.trigger_names()
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_view_count(pycmc_client):
    msg = get.view_count('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res


def test_get_view_names(pycmc_client):
    msg = get.view_names('Contact')
    res = pycmc_client.send_dde_message(msg)
    assert res
