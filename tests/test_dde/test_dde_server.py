from datetime import datetime

from conftest import temp_contact
from pycommence import PyCmcDDEServer
from pycommence.dde.server import DDETopic
from sample_data import TEST_ITEM_NAME, UPDATE_DICT

TESTCOUNT = 2

def test_temp_contact_adds_and_deletes(dde_server, caplog):
    before = count_temp_contact(dde_server)
    assert before == 0, 'Temp contact already exists in view before test'

    with temp_contact(dde_server) as dde_server_temp_contact:
        dde_server = dde_server_temp_contact
        with caplog.at_level('DEBUG'):
            cnt_count = count_temp_contact(dde_server)
            assert cnt_count > 0, 'Temp contact not found in view'
            assert cnt_count < 2, 'Multiple temp contacts found in view'
        print('\nCaptured Logs:')
        for record in caplog.records:
            print(f'{record.levelname}: {record.message}')

    after = count_temp_contact(dde_server)
    assert after == 0, 'Temp contact still exists in view after test'


def count_temp_contact(dde_server: PyCmcDDEServer) -> int:
    dde_server.view_reset('Contact')
    dde_server.view_filter_by_fields('contactKey', TEST_ITEM_NAME)
    cnt_count = dde_server.row_count()
    return cnt_count


def test_edit_item(dde_server):
    with temp_contact(dde_server) as dde_server_temp_contact:
        dde_server = dde_server_temp_contact
        update_dict = UPDATE_DICT
        tstamp = 'Updated on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict['Notes'] = tstamp
        category = 'Contact'
        dde_server.view_reset(category)
        res = dde_server.item_edit(category, TEST_ITEM_NAME, update_dict, DDETopic.VIEW)
        assert res is True

        dde_server.view_reset(category)
        item = dde_server.item_read(category, TEST_ITEM_NAME)
        assert item['Notes'] == tstamp, 'Notes field not updated correctly'
