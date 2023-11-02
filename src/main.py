from cmc_gpt.cmc_cursor import CommenceCursor
from cmc_gpt.cmc_db import CmcDB


def commence_cursor() -> CommenceCursor:
    cmc_db = CmcDB()
    cursor: CommenceCursor = cmc_db.get_cursor('Hire')
    return cursor


def get_a_hire(commence_cursor):
    return commence_cursor.get_query_row_set(1)


cursor = commence_cursor()
rs = cursor.get_query_row_set(1)
...
