from datetime import datetime

from conftest import temp_contact
from pycommence import PyCmcDDEServer
from pycommence.dde.server import DDETopic
from pycommence.pycommence_client import PyCommenceClient
from sample_data import TEST_ITEM_NAME, UPDATE_DICT

TESTCOUNT = 2

def test_temp_contact_adds_and_deletes(pycmc_client, caplog):
    before = count_temp_contact(pycmc_client)
    assert before == 0, 'Temp contact already exists in view before test'

    with temp_contact(pycmc_client):
        with caplog.at_level('DEBUG'):
            cnt_count = count_temp_contact(pycmc_client)
            assert cnt_count > 0, 'Temp contact not found in view'
            assert cnt_count < 2, 'Multiple temp contacts found in view'
        print('\nCaptured Logs:')
        for record in caplog.records:
            print(f'{record.levelname}: {record.message}')

    after = count_temp_contact(pycmc_client)
    assert after == 0, 'Temp contact still exists in view after test'


def count_temp_contact(dde_server: PyCommenceClient) -> int:
    topic = DDETopic.GET
    dde_server.conversation(topic).view_reset('Contact')
    dde_server.conversation().view_filter_by_field('contactKey', TEST_ITEM_NAME)
    cnt_count = dde_server.conversation().row_count()
    return cnt_count


def test_edit_item(pycmc_client: PyCommenceClient):
    with temp_contact(pycmc_client) as pycmc_client_temp_contact:
        pycmc_client = pycmc_client_temp_contact
        update_dict = UPDATE_DICT
        tstamp = 'Updated on ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_dict['Notes'] = tstamp
        category = 'Contact'
        pycmc_client.conversation().view_reset(category)
        res = pycmc_client.item_edit(category, TEST_ITEM_NAME, update_dict, DDETopic.VIEW)
        assert res is True

        pycmc_client.conversation(DDETopic.VIEW).view_reset(category)
        item = pycmc_client.item_read(category, TEST_ITEM_NAME)
        assert item['Notes'] == tstamp, 'Notes field not updated correctly'
