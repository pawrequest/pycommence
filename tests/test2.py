import pytest

from src.cmc_gpt.cmc_cursor import CommenceCursor
from src.cmc_gpt.cmc_db import CmcDB


@pytest.fixture
def commence_cursor() -> CommenceCursor:
    cmc_db = CmcDB()
    cursor: CommenceCursor = cmc_db.get_cursor('Hire')
    yield cursor


def test_get_a_hire(commence_cursor):
    rs = commence_cursor.get_query_row_set(1, 1)
    ...
