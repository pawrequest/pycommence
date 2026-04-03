import contextlib

import pytest
from conftest import Contact
from loguru import logger
from sample_data import JEFF_KEY, NEW_DICT, NEW_KEY, UPDATE_DICT

from pycommence import MoreAvailable
from pycommence.core.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.core.filters import ConditionType, FieldFilter, FilterArray
from pycommence.core.pagination import Pagination
from pycommence.core.row_data import RowData
from pycommence.cursor import CursorAPI
from pycommence.pycommence_client import PyCommenceClient

PAGINATED = Pagination(offset=0, limit=5)


@contextlib.contextmanager
def temp_contact(pycmc: PyCommenceClient):
    logger.info('Adding temp record')
    try:
        pycmc.cursor('Contact').create_row(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        pycmc.cursor('Contact').delete_row(pk=NEW_KEY)
        logger.info('Deleted temp record')


def test_pycmc(test_client):
    assert test_client
    print(next(test_client.cursor('Contact').read_rows(pagination=PAGINATED)))


def test_temp_contact(test_client):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        test_client.cursor('Contact').read_row(pk=NEW_KEY)
    with temp_contact(test_client):
        res = test_client.cursor('Contact').read_row(pk=NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        test_client.cursor('Contact').read_row(pk=NEW_KEY)


def test_read_rows(test_client):
    res = test_client.cursor('Contact').read_rows(pagination=PAGINATED)
    row = next(res)
    assert isinstance(row, RowData)
    assert row.table_model is Contact


def test_get_one_record(test_client: PyCommenceClient):
    with temp_contact(test_client):
        row: RowData = test_client.cursor('Contact').read_row(pk=NEW_KEY)
        contact = row.construct_model()
        assert isinstance(contact, Contact)
        assert row.data.get('Notes') == 'Some Notes'


def test_edit_record(test_client: PyCommenceClient):
    with temp_contact(test_client):
        original = test_client.cursor('Contact').read_row(pk=NEW_KEY).data

        test_client.cursor('Contact').update_row(pk=NEW_KEY, update_pkg=UPDATE_DICT)
        edited = test_client.cursor('Contact').read_row(pk=NEW_KEY).data
        for k, v in UPDATE_DICT.items():
            assert edited[k] == v
        test_client.cursor('Contact').update_row(pk=NEW_KEY, update_pkg=original)
        reverted = test_client.cursor('Contact').read_row(pk=NEW_KEY).data
        assert reverted == original


def test_add_record(test_client: PyCommenceClient):
    row_count1 = test_client.cursor('Contact').row_count
    with temp_contact(test_client):
        test_client.refresh_cursor('Contact')
        row_count2 = test_client.cursor('Contact').row_count
        assert row_count2 == row_count1 + 1

        res = test_client.cursor('Contact').read_row(pk=NEW_KEY).data
        for k, v in NEW_DICT.items():
            assert res[k] == v

    test_client.refresh_cursor('Contact')
    row_count3 = test_client.cursor('Contact').row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(test_client: PyCommenceClient):
    with pytest.raises(PyCommenceExistsError):
        with temp_contact(test_client):
            test_client.cursor('Contact').create_row(create_pkg=NEW_DICT)


def test_multiple_csrs(test_client: PyCommenceClient):
    assert test_client.cursor('Account').category == 'Account'
    assert test_client.cursor('Contact').category == 'Contact'
    ...


def test_with_csr():
    with PyCommenceClient('Contact') as pycmc:
        assert pycmc.cursor('Contact').category == 'Contact'
        ...


# def test_pk_filter(pycmc):
#     with temp_contact(pycmc):
#         cursor = pycmc.csr()
#         pk = NEW_KEY
#         filter_array = cursor.pk_filter_array(pk)
#         with cursor.temporary_filter(filter_array):
#             rows = list(pycmc.read_rows())
#             assert len(rows) == 1
#             assert rows[0]['contactKey'] == pk


def test_temporary_filter(test_client):
    cursor: CursorAPI = test_client.cursor('Contact')
    num_rows = cursor.row_count
    pk_fil = cursor.pk_filter(JEFF_KEY)
    filter_array = FilterArray.from_filters(pk_fil)
    with cursor.temporary_filter(filter_array):
        rows = list(cursor.read_rows())
        assert len(rows) == 1
        assert rows[0].data['contactKey'] == JEFF_KEY
    assert cursor.row_count == num_rows


def test_pk_contains_filter(test_client):
    with temp_contact(test_client):
        cursor = test_client.cursor('Contact')
        partial_pk = 'Some'
        filter_array = cursor.pk_filter(partial_pk, condition=ConditionType.CONTAIN).to_array()
        rows = list(cursor.read_rows(filter_array=filter_array))
        assert len(rows) > 0
        for row in rows:
            assert partial_pk in row.data['contactKey']


def test_multiple_conditions(test_client):
    with temp_contact(test_client):
        filter_array = FilterArray.from_filters(
            FieldFilter(column='contactKey', condition=ConditionType.EQUAL, value='Guy.Some'),
            FieldFilter(column='Title', condition=ConditionType.CONTAIN, value='CEO of SO'),
        )
        rows = list(test_client.cursor('Contact').read_rows(filter_array=filter_array))
        assert len(rows) == 1
        assert rows[0].data['contactKey'] == 'Guy.Some'
        assert rows[0].data['Title'] == 'CEO of SOMmeBix'


def test_pagination(test_client):
    with temp_contact(test_client):
        csr = test_client.cursor('Contact')
        pagination = Pagination(limit=5)
        offest_pag = Pagination(offset=2, limit=1)

        rows = list(csr.read_rows(pagination=pagination))

        row3 = next(csr.read_rows(pagination=offest_pag))
        assert row3.data['contactKey'] == rows[2].data['contactKey']

        row1 = next(csr.read_rows(pagination=Pagination(limit=1)))
        assert row1.data['contactKey'] == rows[0].data['contactKey']


def test_read_rows_more_available(test_client):
    csr = test_client.cursor('Contact')
    total_rows = csr.row_count
    limit = 2
    pagination = Pagination(limit=limit, offset=0)
    rows = list(test_client.cursor('Contact').read_rows(pagination=pagination))
    if total_rows > limit:
        assert isinstance(rows[-1], MoreAvailable)
        more = next(row for row in rows if isinstance(row, MoreAvailable))
        assert more.n_more == total_rows - limit
    else:
        assert not any(isinstance(row, MoreAvailable) for row in rows)
