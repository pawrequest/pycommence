import contextlib

import pytest
from loguru import logger

from pycommence.cursor import CursorAPI
from pycommence.exceptions import PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.filters import ConditionType, FieldFilter, FilterArray
from pycommence.pycmc_types import Pagination
from pycommence.pycommence import PyCommence
from .conftest import JEFF_KEY, NEW_DICT, NEW_KEY, UPDATE_DICT

PAGINATED = Pagination(offset=0, limit=5)


def test_pycmc(pycmc):
    assert pycmc
    for rec in pycmc.read_rows(pagination=PAGINATED):
        print(rec)


@contextlib.contextmanager
def temp_contact(pycmc: PyCommence):
    logger.info('Adding temp record')
    try:
        pycmc.create_row(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        pycmc.delete_row(pk=NEW_KEY)
        logger.info('Deleted temp record')


def test_temp_contact(pycmc):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.read_row(pk=NEW_KEY)
    with temp_contact(pycmc):
        res = pycmc.read_row(pk=NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.read_row(pk=NEW_KEY)


def test_get_records(pycmc):
    res = list(pycmc.read_rows(pagination=PAGINATED))
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pycmc: PyCommence):
    with temp_contact(pycmc):
        res = pycmc.read_row(pk=NEW_KEY)
        assert isinstance(res, dict)
        assert res['Notes'] == 'Some Notes'


def test_edit_record(pycmc: PyCommence):
    with temp_contact(pycmc):
        original = pycmc.read_row(pk=NEW_KEY)

        pycmc.update_row(pk=NEW_KEY, update_pkg=UPDATE_DICT)
        edited = pycmc.read_row(pk=NEW_KEY)
        for k, v in UPDATE_DICT.items():
            assert edited[k] == v

        pycmc.update_row(pk=NEW_KEY, update_pkg=original)
        reverted = pycmc.read_row(pk=NEW_KEY)
        assert reverted == original


def test_add_record(pycmc: PyCommence):
    csr = pycmc.csr()
    row_count1 = csr.row_count
    with temp_contact(pycmc):
        pycmc.refresh_csr(csr)
        row_count2 = pycmc.csr().row_count
        assert row_count2 == row_count1 + 1

        res = pycmc.read_row(pk=NEW_KEY)
        for k, v in NEW_DICT.items():
            assert res[k] == v

    pycmc.refresh_csr(csr)
    row_count3 = pycmc.csr().row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc: PyCommence):
    with pytest.raises(PyCommenceExistsError):
        with temp_contact(pycmc):
            pycmc.create_row(create_pkg=NEW_DICT)


def test_multiple_csrs(pycmc: PyCommence):
    pycmc.set_csr(csrname='Account')
    assert pycmc.csr(csrname='Account').category == 'Account'
    assert pycmc.csr(csrname='Contact').category == 'Contact'


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
    cursor:CursorAPI = pycmc.csr()
    num_rows = cursor.row_count
    pk_fil = cursor.pk_filter(JEFF_KEY)
    filter_array = FilterArray.from_filters(pk_fil)
    with cursor.temporary_filter(filter_array):
        rows = list(pycmc.read_rows())
        assert len(rows) == 1
        assert rows[0]['contactKey'] == JEFF_KEY
    assert cursor.row_count == num_rows


def test_pk_contains_filter(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        partial_pk = 'Some'
        filter_array = cursor.pk_filter(partial_pk, condition=ConditionType.CONTAIN).to_array()
        rows = list(pycmc.read_rows(filter_array=filter_array))
        assert len(rows) > 0
        for row in rows:
            assert partial_pk in row['contactKey']


def test_multiple_conditions(pycmc):
    with temp_contact(pycmc):
        filter_array = FilterArray.from_filters(
            FieldFilter(column='contactKey', condition=ConditionType.EQUAL, value='Guy.Some'),
            FieldFilter(column='Title', condition=ConditionType.CONTAIN, value='CEO of SO'),
        )
        rows = list(pycmc.read_rows(filter_array=filter_array))
        assert len(rows) == 1
        assert rows[0]['contactKey'] == 'Guy.Some'
        assert rows[0]['Title'] == 'CEO of SOMmeBix'




def test_pagination(pycmc):
    with temp_contact(pycmc):
        csr = pycmc.csr()
        pagination = Pagination(limit=5)
        offest_pag = Pagination(offset=2, limit=1)

        rows = tuple(csr._read_rows(pagination=pagination))

        row3 = next(csr._read_rows(pagination=offest_pag))
        assert row3['contactKey'] == rows[2]['contactKey']

        row1 = next(csr._read_rows(pagination=Pagination(limit=1)))
        assert row1['contactKey'] == rows[0]['contactKey']


