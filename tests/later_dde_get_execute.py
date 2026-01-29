from conftest import temp_contact
from pycommence.core.dde_common.execute_msgs import (
    execute_add_shared_item,
    execute_append_text,
    execute_assign_connection,
    execute_check_in_form_script,
    execute_check_out_form_script,
    execute_delete_item,
    execute_delete_view,
    execute_edit_item,
    execute_fire_trigger,
    execute_get_view_to_file,
    execute_log_phone_call,
    execute_merge_template_create,
    execute_merge_template_save,
    execute_promote_item_to_shared,
    execute_show_desktop,
    execute_show_item,
    execute_show_view,
    execute_unassign_connection,
)


def test_execute_add_shared_item(dde_server):
    msg = execute_add_shared_item('Contact', 'TestSharedItem')
    res = dde_server.send_message(msg)
    assert res


def test_execute_append_text(dde_server):
    with temp_contact(dde_server):
        msg = execute_append_text('Contact', 'Musk.Elon', 'Notes', 'TestAAAAAAAAAAAAAA text')
        res = dde_server.send_message(msg)
    assert res


def test_execute_assign_connection(dde_server):
    msg = execute_assign_connection('Contact', 'TestItem', 'RelatedTo', 'Company', 'TestCompany')
    res = dde_server.send_message(msg)
    assert res


def test_execute_unassign_connection(dde_server):
    msg = execute_unassign_connection('Contact', 'TestItem', 'RelatedTo', 'Company', 'TestCompany')
    res = dde_server.send_message(msg)
    assert res


def test_execute_edit_item(dde_server):
    msg = execute_edit_item('Contact', 'TestItem', 'Name', 'UpdatedName')
    res = dde_server.send_message(msg)
    assert res


def test_execute_delete_item(dde_server):
    msg = execute_delete_item('Contact', 'TestItem')
    res = dde_server.send_message(msg)
    assert res


def test_execute_delete_view(dde_server):
    msg = execute_delete_view('TestView')
    res = dde_server.send_message(msg)
    assert res


def test_execute_fire_trigger(dde_server):
    msg = execute_fire_trigger('TestTrigger')
    res = dde_server.send_message(msg)
    assert res


def test_execute_show_desktop(dde_server):
    msg = execute_show_desktop('TestDesktop')
    res = dde_server.send_message(msg)
    assert res


def test_execute_show_item(dde_server):
    msg = execute_show_item('Contact', 'TestItem')
    res = dde_server.send_message(msg)
    assert res


def test_execute_show_view(dde_server):
    msg = execute_show_view('TestView')
    res = dde_server.send_message(msg)
    assert res


def test_execute_get_view_to_file(dde_server):
    msg = execute_get_view_to_file('TestView', 1, None, None, 'test.txt')
    res = dde_server.send_message(msg)
    assert res


def test_execute_check_in_form_script(dde_server):
    msg = execute_check_in_form_script('Contact', 'TestForm', 'test.vbs')
    res = dde_server.send_message(msg)
    assert res


def test_execute_check_out_form_script(dde_server):
    msg = execute_check_out_form_script('Contact', 'TestForm', 'test.vbs')
    res = dde_server.send_message(msg)
    assert res


def test_execute_merge_template_create(dde_server):
    msg = execute_merge_template_create('TestTemplate', 'Contact', False)
    res = dde_server.send_message(msg)
    assert res


def test_execute_merge_template_save(dde_server):
    msg = execute_merge_template_save('TestTemplate', False)
    res = dde_server.send_message(msg)
    assert res


def test_execute_promote_item_to_shared(dde_server):
    msg = execute_promote_item_to_shared('Contact', 'TestItem')
    res = dde_server.send_message(msg)
    assert res


def test_execute_log_phone_call(dde_server):
    msg = execute_log_phone_call('Contact', 'TestItem', 'Company', 'TestCompany')
    res = dde_server.send_message(msg)
    assert res
