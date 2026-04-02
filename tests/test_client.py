from datetime import datetime

from conftest import temp_contact
from sample_data import TEST_ITEM_NAME, UPDATE_DICT

from pycommence.dde import DDETopic
from pycommence.dde.msgs import system
from pycommence.pycommence_client import PyCommenceClient


def test_client_system(test_client):
    msg = system.status()
    res = test_client.send_dde_message(msg)
    ...


TESTCOUNT = 2


def test_temp_contact_adds_and_deletes(test_client, caplog):
    before = count_temp_contact(test_client)
    assert before == 0, 'Temp contact already exists in view before test'

    with temp_contact(test_client):
        with caplog.at_level('DEBUG'):
            cnt_count = count_temp_contact(test_client)
            assert cnt_count > 0, 'Temp contact not found in view'
            assert cnt_count < 2, 'Multiple temp contacts found in view'
        print('\nCaptured Logs:')
        for record in caplog.records:
            print(f'{record.levelname}: {record.message}')

    after = count_temp_contact(test_client)
    assert after == 0, 'Temp contact still exists in view after test'


def count_temp_contact(dde_server: PyCommenceClient) -> int:
    topic = DDETopic.GET
    dde_server.conversation(topic).view_reset('Contact')
    dde_server.conversation().view_filter_by_field('contactKey', TEST_ITEM_NAME)
    cnt_count = dde_server.conversation().row_count()
    return cnt_count


def test_edit_item(test_client: PyCommenceClient):
    with temp_contact(test_client) as pycmc_client_temp_contact:
        test_client = pycmc_client_temp_contact
        update_dict = UPDATE_DICT
        tstamp = 'Updated on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict['Notes'] = tstamp
        category = 'Contact'
        test_client.conversation().view_reset(category)
        res = test_client.item_edit_dde(category, TEST_ITEM_NAME, update_dict, DDETopic.VIEW)
        assert res is True

        test_client.conversation(DDETopic.VIEW).view_reset(category)
        item = test_client.item_read_dde(category, TEST_ITEM_NAME)
        assert item['Notes'] == tstamp, 'Notes field not updated correctly'


def test_get_category_field_def(test_client: PyCommenceClient, timed):
    category = 'Contact'
    res = test_client.conversation().category_field_definitions(category)
    ...
