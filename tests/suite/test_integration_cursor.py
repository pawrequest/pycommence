"""Integration tests for CursorAPI (requires live Commence)."""

import pytest

from pycommence.core.filters import ConditionType, FieldFilter, FilterArray
from pycommence.core.pagination import MoreAvailable, Pagination
from pycommence.core.row_data import RowData
from pycommence.cursor import CursorAPI
from pycommence.pycommence_client import PyCommence

pytestmark = pytest.mark.integration


class TestCursorProperties:
    def test_category_name(self, contact_cursor: CursorAPI):
        assert contact_cursor.category == 'Contact'

    def test_row_count_positive(self, contact_cursor: CursorAPI):
        assert contact_cursor.row_count > 0

    def test_column_count_positive(self, contact_cursor: CursorAPI):
        assert contact_cursor.column_count > 0

    def test_pk_label(self, contact_cursor: CursorAPI):
        label = contact_cursor.pk_label
        assert isinstance(label, str)
        assert len(label) > 0


class TestCursorReadRows:
    def test_read_rows_returns_generator(self, contact_cursor: CursorAPI):
        rows = contact_cursor.read_rows(pagination=Pagination(limit=5))
        row_list = list(rows)
        assert len(row_list) > 0

    def test_read_rows_row_data(self, contact_cursor: CursorAPI):
        rows = list(contact_cursor.read_rows(pagination=Pagination(limit=2)))
        for row in rows:
            if isinstance(row, RowData):
                assert row.category == 'Contact'
                assert isinstance(row.data, dict)
                assert row.row_id

    def test_read_rows_with_limit(self, contact_cursor: CursorAPI):
        rows = [r for r in contact_cursor.read_rows(pagination=Pagination(limit=3)) if isinstance(r, RowData)]
        assert len(rows) <= 3

    def test_read_rows_more_available(self, contact_cursor: CursorAPI):
        # Request 1 row when there are more
        results = list(contact_cursor.read_rows(pagination=Pagination(limit=1)))
        if contact_cursor.row_count > 1:
            assert any(isinstance(r, MoreAvailable) for r in results)


class TestCursorReadRow:
    def test_read_row_by_pk(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        row = csr.read_row(pk=temp_contact)
        assert isinstance(row, RowData)
        assert row.category == 'Contact'


class TestCursorPkOperations:
    def test_pk_exists_true(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        assert csr.pk_exists(temp_contact)

    def test_pk_exists_false(self, contact_cursor: CursorAPI):
        assert not contact_cursor.pk_exists('__DEFINITELY_NOT_A_REAL_CONTACT__')

    def test_pk_to_id_and_back(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        row_id = csr.pk_to_id(temp_contact)
        assert isinstance(row_id, str)
        pk_back = csr.row_id_to_pk(row_id)
        assert pk_back == temp_contact


class TestCursorFiltering:
    def test_temporary_filter(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        fil = FilterArray.from_filters(
            FieldFilter(column=csr.pk_label, condition=ConditionType.EQUAL, value=temp_contact)
        )
        with csr.temporary_filter(fil):
            assert csr.row_count == 1

    def test_filter_cleared_after_context(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        original_count = csr.row_count
        fil = FilterArray.from_filters(
            FieldFilter(column=csr.pk_label, condition=ConditionType.EQUAL, value=temp_contact)
        )
        with csr.temporary_filter(fil):
            pass
        assert csr.row_count == original_count


class TestCursorCRUD:
    def test_create_and_delete(self, pycmc: PyCommence):
        import uuid

        name = f'_PyCmcCRUD_{uuid.uuid4().hex[:6]}'
        csr = pycmc.cursor('Contact')
        pk_label = csr.pk_label

        # CREATE
        created = csr.create_row({pk_label: name})
        assert created is True

        # VERIFY
        assert csr.pk_exists(name)

        # DELETE
        deleted = csr.delete_row(pk=name)
        assert deleted is True
        assert not csr.pk_exists(name)

    def test_update_row(self, pycmc: PyCommence, temp_contact: str):
        csr = pycmc.cursor('Contact')
        updated = csr.update_row({'firstName': 'TestUpdated'}, pk=temp_contact)
        assert updated is True
        row = csr.read_row(pk=temp_contact)
        assert row.data.get('firstName') == 'TestUpdated'
