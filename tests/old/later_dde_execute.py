# from conftest import temp_contact
# from pycommence.dde.msgs.execute import (
#     execute_add_shared_item,
#     execute_append_text,
#     execute_assign_connection,
#     execute_check_in_form_script,
#     execute_check_out_form_script,
#     execute_delete_item,
#     execute_delete_view,
#     execute_edit_item,
#     execute_fire_trigger,
#     execute_get_view_to_file,
#     execute_log_phone_call,
#     execute_merge_template_create,
#     execute_merge_template_save,
#     execute_promote_item_to_shared,
#     execute_show_desktop,
#     execute_show_item,
#     execute_show_view,
#     execute_unassign_connection,
# )
#
#
# def test_execute_add_shared_item(pycmc_client):
#     msg = execute_add_shared_item('Contact', 'TestSharedItem')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_append_text(pycmc_client):
#     with temp_contact(pycmc_client):
#         msg = execute_append_text('Contact', 'Musk.Elon', 'Notes', 'TestAAAAAAAAAAAAAA text')
#         res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_assign_connection(pycmc_client):
#     msg = execute_assign_connection('Contact', 'TestItem', 'RelatedTo', 'Company', 'TestCompany')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_unassign_connection(pycmc_client):
#     msg = execute_unassign_connection('Contact', 'TestItem', 'RelatedTo', 'Company', 'TestCompany')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_edit_item(pycmc_client):
#     msg = execute_edit_item('Contact', 'TestItem', 'Name', 'UpdatedName')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_delete_item(pycmc_client):
#     msg = execute_delete_item('Contact', 'TestItem')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_delete_view(pycmc_client):
#     msg = execute_delete_view('TestView')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_fire_trigger(pycmc_client):
#     msg = execute_fire_trigger('TestTrigger')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_show_desktop(pycmc_client):
#     msg = execute_show_desktop('TestDesktop')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_show_item(pycmc_client):
#     msg = execute_show_item('Contact', 'TestItem')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_show_view(pycmc_client):
#     msg = execute_show_view('TestView')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_get_view_to_file(pycmc_client):
#     msg = execute_get_view_to_file('TestView', 1, None, None, 'test.txt')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_check_in_form_script(pycmc_client):
#     msg = execute_check_in_form_script('Contact', 'TestForm', 'test.vbs')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_check_out_form_script(pycmc_client):
#     msg = execute_check_out_form_script('Contact', 'TestForm', 'test.vbs')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_merge_template_create(pycmc_client):
#     msg = execute_merge_template_create('TestTemplate', 'Contact', False)
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_merge_template_save(pycmc_client):
#     msg = execute_merge_template_save('TestTemplate', False)
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_promote_item_to_shared(pycmc_client):
#     msg = execute_promote_item_to_shared('Contact', 'TestItem')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
#
#
# def test_execute_log_phone_call(pycmc_client):
#     msg = execute_log_phone_call('Contact', 'TestItem', 'Company', 'TestCompany')
#     res = pycmc_client.send_dde_message(msg)
#     assert res
