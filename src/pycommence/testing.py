import pytest

from pycommence.pycommence_client import PyCommence
from pycommence.threads import com_context


@pytest.fixture(scope='function')
def test_client():
    with com_context(), PyCommence() as client:
        if not client.conversation().db_name_and_path()[0] == 'Tutorial':
            raise ValueError('Expected Tutorial DB')
        yield client


@pytest.fixture(scope='function')
def test_client_non_tutorial():
    with com_context(), PyCommence() as client:
        yield client
