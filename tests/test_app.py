import pytest
from starlette.testclient import TestClient

from conftest import Contact
from pycommence.conversation import get_or_create_table_type
from pycommence.fapi.app import app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


def test_status_endpoint(client):
    response = client.get('/status')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_get_one(client):
    response = client.get('/get', params={'csrname': 'Contact', 'pk_value': 'Bezos.Jeff'})
    assert response.status_code == 200
    row_data = response.json()
    data_dict = row_data['data']
    assert data_dict['firstName'] == 'Jeff'
    contact = Contact(row_id=row_data['row_id'], **data_dict)
    assert contact.firstName == 'Jeff'
    ...


# def test_get_one_auto(client):
#     response = client.get('/get', params={'csrname': 'Contact', 'pk_value': 'Bezos.Jeff', 'auto_model': 'true'})
#     assert response.status_code == 200
#     row_data = response.json()
#     data_dict = row_data['data']
#     assert data_dict['firstName'] == 'Jeff'
#     contact = Contact.model_validate(data_dict)
#     assert contact.firstName == 'Jeff'
#     ...


def test_search_endpoint(client):
    response = client.get('/search', params={'csrname': 'Contact', 'pk_value': 'Mark'})
    data = response.json()
    assert response.status_code == 200
    assert 'records' in data
    assert len(data['records']) == 2
