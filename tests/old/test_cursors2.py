import contextlib

import pytest
from loguru import logger

from conftest import Contact
from pycommence.cursor import CursorAPI
from pycommence.core.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.core.filters import ConditionType, FieldFilter, FilterArray
from pycommence.core.pagination import Pagination
from pycommence import MoreAvailable
from bench.client import PyCommence
from pycommence.core.row_data import RowData
from pycommence.icommence.const import CursorType
from pycommence.pycommence_client import PyCommenceClient
from sample_data import JEFF_KEY, NEW_DICT, NEW_KEY, UPDATE_DICT

PAGINATED = Pagination(offset=0, limit=5)


def test_pycmc(pycmc_client):
    assert pycmc_client
    for rec in pycmc_client.cursor('Contact').read_rows(pagination=PAGINATED):
        print(rec)


@contextlib.contextmanager
def temp_contact(contact_cursor: CursorAPI):
    logger.info('Adding temp record')
    try:
        contact_cursor.create_row(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        contact_cursor.delete_row(pk=NEW_KEY)
        logger.info('Deleted temp record')


@contextlib.contextmanager
def temp_contact_client(client: PyCommenceClient):
    logger.info('Adding temp record')
    contact_cursor = client.cursor('Contact')
    try:
        contact_cursor.create_row(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        contact_cursor.delete_row(pk=NEW_KEY)
        logger.info('Deleted temp record')


def test_temp_contact(pycmc_client):
    """Test add_record and delete_record."""
    contact_cursor = pycmc_client.cursor('Contact')
    with pytest.raises(PyCommenceNotFoundError):
        contact_cursor.read_row(pk=NEW_KEY)
    with temp_contact(contact_cursor):
        res = contact_cursor.read_row(pk=NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        contact_cursor.read_row(pk=NEW_KEY)


def test_read_rows(contact_cursor):
    res = contact_cursor.read_rows(pagination=PAGINATED)
    row = next(res)
    assert isinstance(row, RowData)
    assert row.table_model is Contact


def test_get_one_record(contact_cursor):
    with temp_contact(contact_cursor):
        row: RowData = contact_cursor.read_row(pk=NEW_KEY)
        contact = row.construct_model()
        assert isinstance(contact, Contact)
        assert row.data.get('Notes') == 'Some Notes'


def test_edit_record(contact_cursor: CursorAPI):
    excludes = {'row_id', 'category'}
    with temp_contact(contact_cursor):
        original = contact_cursor.read_row(pk=NEW_KEY).data

        contact_cursor.update_row(pk=NEW_KEY, update_pkg=UPDATE_DICT)
        edited = contact_cursor.read_row(pk=NEW_KEY).data
        for k, v in UPDATE_DICT.items():
            assert edited[k] == v
        contact_cursor.update_row(pk=NEW_KEY, update_pkg=original)
        reverted = contact_cursor.read_row(pk=NEW_KEY).data
        assert reverted == original


def test_add_record(pycmc_client):
    contact_cursor = pycmc_client.cursor('Contact')
    row_count1 = contact_cursor.row_count
    with temp_contact_client(pycmc_client):
        contact_cursor = pycmc_client.refresh_cursor()
        row_count2 = contact_cursor.row_count
        assert row_count2 == row_count1 + 1

        row_id = contact_cursor.pk_to_id(NEW_KEY)

        res = contact_cursor.read_row(row_id=row_id).data
        for k, v in NEW_DICT.items():
            assert res[k] == v

    pycmc_client.refresh_cursor()
    contact_cursor = pycmc_client.refresh_cursor()
    row_count3 = contact_cursor.row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc: PyCommence):
    with pytest.raises(PyCommenceExistsError):
        with temp_contact(pycmc):
            pycmc.create_row(create_pkg=NEW_DICT)


def test_multiple_csrs(pycmc: PyCommence):
    pycmc.set_csr(csrname='Account')
    assert pycmc.csr(csrname='Account').category == 'Account'
    assert pycmc.csr(csrname='Contact').category == 'Contact'
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


def test_temporary_filter(pycmc):
    cursor: CursorAPI = pycmc.csr()
    num_rows = cursor.row_count
    pk_fil = cursor.pk_filter(JEFF_KEY)
    filter_array = FilterArray.from_filters(pk_fil)
    with cursor.temporary_filter(filter_array):
        rows = list(pycmc.read_rows())
        assert len(rows) == 1
        assert rows[0].data['contactKey'] == JEFF_KEY
    assert cursor.row_count == num_rows


def test_pk_contains_filter(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        partial_pk = 'Some'
        filter_array = cursor.pk_filter(partial_pk, condition=ConditionType.CONTAIN).to_array()
        rows = list(pycmc.read_rows(filter_array=filter_array))
        assert len(rows) > 0
        for row in rows:
            assert partial_pk in row.data['contactKey']


def test_multiple_conditions(pycmc):
    with temp_contact(pycmc):
        filter_array = FilterArray.from_filters(
            FieldFilter(column='contactKey', condition=ConditionType.EQUAL, value='Guy.Some'),
            FieldFilter(column='Title', condition=ConditionType.CONTAIN, value='CEO of SO'),
        )
        rows = list(pycmc.read_rows(filter_array=filter_array))
        assert len(rows) == 1
        assert rows[0].data['contactKey'] == 'Guy.Some'
        assert rows[0].data['Title'] == 'CEO of SOMmeBix'


def test_pagination(pycmc):
    with temp_contact(pycmc):
        csr = pycmc.csr()
        pagination = Pagination(limit=5)
        offest_pag = Pagination(offset=2, limit=1)

        rows = list(csr.read_rows(pagination=pagination))

        row3 = next(csr.read_rows(pagination=offest_pag))
        assert row3.data['contactKey'] == rows[2].data['contactKey']

        row1 = next(csr.read_rows(pagination=Pagination(limit=1)))
        assert row1.data['contactKey'] == rows[0].data['contactKey']


def test_read_rows_more_available(pycmc):
    csr = pycmc.csr()
    total_rows = csr.row_count
    limit = 2
    pagination = Pagination(limit=limit, offset=0)
    rows = list(pycmc.read_rows(pagination=pagination))
    if total_rows > limit:
        assert isinstance(rows[-1], MoreAvailable)
        more = next(row for row in rows if isinstance(row, MoreAvailable))
        assert more.n_more == total_rows - limit
    else:
        assert not any(isinstance(row, MoreAvailable) for row in rows)


@pytest.fixture
def pycmc_view():
    pycmc = PyCommence()
    pycmc.set_csr('Contact List', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def test_view(pycmc_view):
    rows = pycmc_view.read_rows()
    print(len(list(rows)), 'records')
