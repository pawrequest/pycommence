import pytest

from cmc_gpt.cmc_db import CmcDB


@pytest.fixture
def commence_cursor():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Hire')
    yield cursor

def test_get_a_hire(commence_cursor):



