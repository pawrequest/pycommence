import contextlib

import pytest
from loguru import logger

from pycommence.exceptions import PyCommenceError, PyCommenceExistsError, PyCommenceNotFoundError
from pycommence.filters import ConditionType, FieldFilter, FilterArray
from pycommence.pycommence_v2 import PyCommence
from .conftest import NEW_DICT, NEW_KEY, UPDATE_DICT


def test_pycmc(pycmc):
    assert pycmc
    for rec in pycmc.csr().rows(3):
        print(rec)


@contextlib.contextmanager
def temp_contact(pycmc: PyCommence):
    try:
        pycmc.csr().create_row_by_pkg(create_pkg=NEW_DICT)
        logger.info('Added temp record')
        yield
    finally:
        for row_id in pycmc.csr().pk_to_row_ids(NEW_KEY):
            logger.info('Deleted temp record')
            pycmc.csr().delete_row_by_id(row_id)


def test_temp_contact(pycmc):
    """Test add_record and delete_record."""
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.csr().read_one_row_pk(NEW_KEY)
    with temp_contact(pycmc):
        res = pycmc.csr().read_one_row_pk(NEW_KEY)
        assert res
    with pytest.raises(PyCommenceNotFoundError):
        pycmc.csr().read_one_row_pk(NEW_KEY)


def test_get_records(pycmc):
    res = list(pycmc.csr().rows(2))
    assert isinstance(res, list)
    assert isinstance(res[0], dict)


def test_get_one_record(pycmc: PyCommence):
    with temp_contact(pycmc):
        res = pycmc.csr().read_one_row_pk(NEW_KEY)
        assert isinstance(res, dict)
        assert res['Notes'] == 'Some Notes'


def test_edit_record(pycmc: PyCommence):
    with temp_contact(pycmc):
        csr = pycmc.csr()
        original = csr.read_one_row_pk(NEW_KEY, with_id=False, with_category=False)

        csr.update_row_by_pk(pk=NEW_KEY, update_pkg=UPDATE_DICT)
        edited = csr.read_one_row_pk(NEW_KEY, with_category=False, with_id=False)
        for k, v in UPDATE_DICT.items():
            assert edited[k] == v

        csr.update_row_by_pk(pk=NEW_KEY, update_pkg=original)
        reverted = csr.read_one_row_pk(NEW_KEY, with_id=False, with_category=False)
        assert reverted == original


def test_add_record(pycmc: PyCommence):
    csr = pycmc.csr()
    row_count1 = csr.row_count
    with temp_contact(pycmc):
        pycmc.refresh_csr(csr)
        row_count2 = pycmc.csr().row_count
        assert row_count2 == row_count1 + 1

        res = pycmc.csr().read_one_row_pk(NEW_KEY)
        for k, v in NEW_DICT.items():
            assert res[k] == v

    pycmc.refresh_csr(csr)
    row_count3 = pycmc.csr().row_count
    assert row_count3 == row_count1


def test_add_duplicate_raises(pycmc: PyCommence):
    with pytest.raises(PyCommenceExistsError):
        with temp_contact(pycmc):
            pycmc.csr().create_row_by_pkg(create_pkg=NEW_DICT)


def test_multiple_csrs(pycmc: PyCommence):
    assert pycmc
    pycmc.set_csr(csrname='Account')
    assert pycmc.csr(csrname='Account').category == 'Account'
    [print(pycmc.csr(key).row_count, f'{key} records') for key in pycmc.csrs.keys()]


# def test_add_related(pycmc: PyCommence):
#     connection = Connection2(
#         name='Relates To',
#         category='Account',
#         column='customerNumber',
#     )
#     allcols = pycmc.csr().headers
#     col_count = pycmc.csr().column_count
#     pycmc.csr().add_related_column(connection)
#     assert pycmc.csr().column_count == col_count + 1


### gpt
def test_pk_filter(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        pk = 'Some.Guy'
        filter_array = cursor.pk_filter(pk)
        cursor.filter_by_array(filter_array)
        rows = list(cursor.rows())
        assert len(rows) == 1
        assert rows[0]['contactKey'] == pk


def test_pk_contains_filter(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        partial_pk = 'Some'
        filter_array = cursor.pk_contains_filter(partial_pk)
        cursor.filter_by_array(filter_array)
        rows = list(cursor.rows())
        assert len(rows) > 0
        for row in rows:
            assert partial_pk in row['contactKey']


def test_temporary_filter(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        pk = 'Some.Guy'
        filter_array = cursor.pk_filter(pk)
        with cursor.temporary_filter(filter_array):
            rows = list(cursor.rows())
            assert len(rows) == 1
            assert rows[0]['contactKey'] == pk
        assert not cursor.filter_array  # Ensures filters are cleared


def test_multiple_conditions(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        filter_array = FilterArray.from_filters(
            FieldFilter(column='contactKey', condition=ConditionType.EQUAL, value='Some.Guy'),
            FieldFilter(column='Title', condition=ConditionType.EQUAL, value='CEO of SOMmeBix'),
        )
        cursor.filter_by_array(filter_array)
        rows = list(cursor.rows())
        assert len(rows) == 1
        assert rows[0]['contactKey'] == 'Some.Guy'
        assert rows[0]['Title'] == 'CEO of SOMmeBix'


def test_clear_all_filters(pycmc):
    with temp_contact(pycmc):
        cursor = pycmc.csr()
        pk = 'Some.Guy'
        filter_array = cursor.pk_filter(pk)
        cursor.filter_by_array(filter_array)
        rows = list(cursor.rows())
        assert len(rows) == 1
        cursor.clear_all_filters()
        assert not cursor.filter_array


def test_filter_combination(pycmc):
    cursor = pycmc.csr()
    filter_array = FilterArray.from_filters(
        FieldFilter(column='contactKey', condition=ConditionType.EQUAL, value='Some.Guy'),
        FieldFilter(column='Notes', condition=ConditionType.CONTAIN, value='Notes'),
    )
    cursor.filter_by_array(filter_array)
    rows = list(cursor.rows())
    assert len(rows) == 1
    assert rows[0]['contactKey'] == 'Some.Guy'
    assert 'Notes' in rows[0]['Notes']
