import pytest

from pycommence.dde import DDEMessageBase, DDETopic
from pycommence.dde.msgs import get

TESTCOUNT = 34 + 3


def test_msg(test_client):
    msg = DDEMessageBase(func_name='GetFieldCount', params=['Contact'], topic=DDETopic.GET)
    res = test_client.send_dde_message(msg)
    assert res == '45'


####


def test_clarify_item_names(test_client):
    msg = get.clarify_item_names()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_active_view_info(test_client):
    msg = get.active_view_info()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_caller_id(test_client):
    msg = get.caller_id('Contact', '412-555-7890')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_category_count(test_client):
    msg = get.category_count()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_category_definition(test_client, timed):
    msg = get.category_definition('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_category_names(test_client):
    msg = get.category_names()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_connection_count(test_client):
    msg = get.connection_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_connection_names(test_client):
    msg = get.connection_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_database(test_client):
    msg = get.database()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_database_definition(test_client):
    msg = get.database_definition()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_desktop_count(test_client):
    msg = get.desktop_count()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_desktop_names(test_client):
    msg = get.desktop_names()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_field(test_client):
    msg = get.field('Contact', 'Musk.Elon', 'Name')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_fields(test_client):
    msg = get.fields('Contact', 'Musk.Elon', ['firstName', 'lastName'])
    res = test_client.send_dde_message(msg)
    assert res == ['Elon', 'Musk']


def test_get_field_count(test_client):
    msg = get.field_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_field_definition(test_client):
    msg = get.field_definition('Contact', 'firstName')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_field_names(test_client):
    msg = get.field_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_field_to_file(test_client):
    msg = get.field_to_file('Contact', 'Musk.Elon', 'Name', 'test.txt')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_form_count(test_client):
    msg = get.form_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_form_names(test_client):
    msg = get.form_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_image_field_count(test_client):
    msg = get.image_field_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_names(test_client):
    msg = get.image_field_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_to_file(test_client):
    msg = get.image_field_to_file('Contact', '1', 'Photo', 'test.jpg')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_item_count(test_client):
    msg = get.item_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_item_names(test_client):
    msg = get.item_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_last_error(test_client):
    msg = get.last_error()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_mark_item(test_client):
    msg = get.mark_item('Contact', 'Musk.Elon')
    res = test_client.send_dde_message(msg)
    assert res


def test_mark_active_item(test_client):
    msg = get.mark_active_item()
    res = test_client.send_dde_message(msg)
    assert res


@pytest.mark.skip(reason='Requires TAPI setup')
def test_get_phone_number(test_client):
    msg = get.phone_number('412-555-7890')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_preference(test_client):
    msg = get.preference('ME')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_reverse_name(test_client):
    msg = get.reverse_name('John Doe')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_trigger_count(test_client):
    msg = get.trigger_count()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_trigger_names(test_client):
    msg = get.trigger_names()
    res = test_client.send_dde_message(msg)
    assert res


def test_get_view_count(test_client):
    msg = get.view_count('Contact')
    res = test_client.send_dde_message(msg)
    assert res


def test_get_view_names(test_client):
    msg = get.view_names('Contact')
    res = test_client.send_dde_message(msg)
    assert res
