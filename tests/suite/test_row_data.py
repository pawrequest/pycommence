"""Tests for pycommence.core.row_data"""

from pycommence.core.row_data import RowData, RowInfo


class TestRowInfo:
    def test_named_tuple(self):
        ri = RowInfo(category='Contact', row_id='ABC123')
        assert ri.category == 'Contact'
        assert ri.row_id == 'ABC123'


class TestRowData:
    def test_creation(self):
        rd = RowData(category='Contact', row_id='R1', data={'Name': 'Alice'})
        assert rd.category == 'Contact'
        assert rd.data['Name'] == 'Alice'
