import pytest
from starlette.testclient import TestClient

from .conftest import Contact
from pycommence.fapi.app import app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


def test_status_endpoint(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_one(client):
    response = client.get("/get", params={"csrname": 'Contact', "pk_value": "Bezos.Jeff"})
    data = response.json()
    assert response.status_code == 200
    assert data['row_id']
    contact = Contact.model_validate(data)
    assert contact.firstName == "Jeff"
    ...


def test_search_endpoint(client):
    response = client.get("/search", params={"csrname": 'Contact', "pk_value": "Mark"})
    data = response.json()
    assert response.status_code == 200
    assert 'records' in data
    assert len(data['records']) == 2
