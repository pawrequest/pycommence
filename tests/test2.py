import pytest



@pytest.fixture
def commence_cursor() -> CmcCsr:
    cmc_db = CmcDB()
    cursor: CmcCsr = cmc_db.get_cursor('Hire')
    yield cursor


def test_get_a_hire(commence_cursor):
    rs = commence_cursor.get_query_row_set(1, 1)
    ...
