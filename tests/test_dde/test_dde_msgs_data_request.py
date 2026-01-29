import pytest

from pycommence.dde.server import DDEMessageBase, DDETopic
from pycommence.dde.msgs.get import (
    clarify_item_names,
    get_active_view_info,
    get_caller_id,
    get_category_count,
    get_category_definition,
    get_category_names,
    get_connection_count,
    get_connection_names,
    get_database,
    get_database_definition,
    get_desktop_count,
    get_desktop_names,
    get_field,
    get_field_count,
    get_field_definition,
    get_field_names,
    get_field_to_file,
    get_fields,
    get_form_count,
    get_form_names,
    get_image_field_count,
    get_image_field_names,
    get_image_field_to_file,
    get_item_count,
    get_item_names,
    get_last_error,
    get_mark_item,
    get_phone_number,
    get_preference,
    get_reverse_name,
    get_trigger_count,
    get_trigger_names,
    get_view_count,
    get_view_names,
    mark_active_item,
)

TESTCOUNT = 34 + 3

def test_msg(dde_server):
    msg = DDEMessageBase(func_name='GetFieldCount', params=['Contact'], topic=DDETopic.GET)
    res = dde_server.send_message(msg)
    assert res == '45'


####

def test_clarify_item_names(dde_server):
    msg = clarify_item_names()
    res = dde_server.send_message(msg)
    assert res


def test_get_active_view_info(dde_server):
    msg = get_active_view_info()
    res = dde_server.send_message(msg)
    assert res


def test_get_caller_id(dde_server):
    msg = get_caller_id('Contact', '412-555-7890')
    res = dde_server.send_message(msg)
    assert res


def test_get_category_count(dde_server):
    msg = get_category_count()
    res = dde_server.send_message(msg)
    assert res


def test_get_category_definition(dde_server):
    msg = get_category_definition('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_category_names(dde_server):
    msg = get_category_names()
    res = dde_server.send_message(msg)
    assert res


def test_get_connection_count(dde_server):
    msg = get_connection_count('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_connection_names(dde_server):
    msg = get_connection_names('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_database(dde_server):
    msg = get_database()
    res = dde_server.send_message(msg)
    assert res


def test_get_database_definition(dde_server):
    msg = get_database_definition()
    res = dde_server.send_message(msg)
    assert res


def test_get_desktop_count(dde_server):
    msg = get_desktop_count()
    res = dde_server.send_message(msg)
    assert res


def test_get_desktop_names(dde_server):
    msg = get_desktop_names()
    res = dde_server.send_message(msg)
    assert res


def test_get_field(dde_server):
    msg = get_field('Contact', 'Musk.Elon', 'Name')
    res = dde_server.send_message(msg)
    assert res


def test_get_fields(dde_server):
    msg = get_fields('Contact', 'Musk.Elon', ['firstName', 'lastName'])
    res = dde_server.send_message(msg)
    assert res == ['Elon', 'Musk']


def test_get_fields2(dde_server):
    res = dde_server.category_field_names('Contact')
    ...


def test_get_field_count(dde_server):
    msg = get_field_count('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_field_definition(dde_server):
    msg = get_field_definition('Contact', 'firstName')
    res = dde_server.send_message(msg)
    assert res


def test_get_field_names(dde_server):
    msg = get_field_names('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_field_to_file(dde_server):
    msg = get_field_to_file('Contact', 'Musk.Elon', 'Name', 'test.txt')
    res = dde_server.send_message(msg)
    assert res


def test_get_form_count(dde_server):
    msg = get_form_count('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_form_names(dde_server):
    msg = get_form_names('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_image_field_count(dde_server):
    msg = get_image_field_count('Contact')
    res = dde_server.send_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_names(dde_server):
    msg = get_image_field_names('Contact')
    res = dde_server.send_message(msg)
    assert res


@pytest.mark.skip(reason='No image fields in test db')
def test_get_image_field_to_file(dde_server):
    msg = get_image_field_to_file('Contact', '1', 'Photo', 'test.jpg')
    res = dde_server.send_message(msg)
    assert res


def test_get_item_count(dde_server):
    msg = get_item_count('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_item_names(dde_server):
    msg = get_item_names('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_last_error(dde_server):
    msg = get_last_error()
    res = dde_server.send_message(msg)
    assert res


def test_get_mark_item(dde_server):
    msg = get_mark_item('Contact', 'Musk.Elon')
    res = dde_server.send_message(msg)
    assert res


def test_mark_active_item(dde_server):
    msg = mark_active_item()
    res = dde_server.send_message(msg)
    assert res


@pytest.mark.skip(reason='Requires TAPI setup')
def test_get_phone_number(dde_server):
    msg = get_phone_number('412-555-7890')
    res = dde_server.send_message(msg)
    assert res


def test_get_preference(dde_server):
    msg = get_preference('ME')
    res = dde_server.send_message(msg)
    assert res


def test_get_reverse_name(dde_server):
    msg = get_reverse_name('John Doe')
    res = dde_server.send_message(msg)
    assert res


def test_get_trigger_count(dde_server):
    msg = get_trigger_count()
    res = dde_server.send_message(msg)
    assert res


def test_get_trigger_names(dde_server):
    msg = get_trigger_names()
    res = dde_server.send_message(msg)
    assert res


def test_get_view_count(dde_server):
    msg = get_view_count('Contact')
    res = dde_server.send_message(msg)
    assert res


def test_get_view_names(dde_server):
    msg = get_view_names('Contact')
    res = dde_server.send_message(msg)
    assert res
