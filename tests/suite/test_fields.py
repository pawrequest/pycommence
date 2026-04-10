"""Tests for pycommence.core.fields"""

from pycommence.core.fields import (
    DATA_TYPES,
    CmcDataType,
    CmcDefsDict,
    CmcFieldDefinition,
    parse_info_str,
)


class TestCmcDataType:
    def test_lookup_by_int(self):
        dt = CmcDataType.lookup_datatype(0)
        assert dt.alias == 'TEXT'

    def test_lookup_by_alias(self):
        dt = CmcDataType.lookup_datatype('NUMBER')
        assert dt.int_value == 1

    def test_lookup_by_alias_case_insensitive(self):
        dt = CmcDataType.lookup_datatype('checkbox')
        assert dt.int_value == 7

    def test_lookup_unknown_int(self):
        dt = CmcDataType.lookup_datatype(999)
        assert dt.alias == 'ERROR'

    def test_lookup_unknown_str(self):
        dt = CmcDataType.lookup_datatype('NONSENSE')
        assert dt.alias == 'ERROR'

    def test_unknown_factory(self):
        dt = CmcDataType.unknown()
        assert dt.int_value == -1

    def test_all_data_types_have_py_type(self):
        for dt in DATA_TYPES:
            assert dt.py_type is not None


class TestParseInfoStr:
    def test_basic(self):
        info = 'TEXT;*;%0000000000;*;%100;*;%default'
        default, ftype, flags, maxc = parse_info_str(info)
        assert ftype == 'TEXT'
        assert maxc == '100'

    def test_list_input(self):
        info = ['NUMBER', '0000010000', '50', '0']
        default, ftype, flags, maxc = parse_info_str(info)
        assert ftype == 'NUMBER'


class TestCmcFieldDefinition:
    def test_connection_field(self):
        fd = CmcFieldDefinition.connection_field()
        assert fd.type.alias == 'CONNECTION'

    def test_error_field(self):
        fd = CmcFieldDefinition.error_field()
        assert fd.type.alias == 'ERROR'


class TestCmcDefsDict:
    def test_py_types_dict(self):
        dd = CmcDefsDict()
        dd['myfield'] = CmcFieldDefinition(
            type=CmcDataType.lookup_datatype('TEXT'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=100,
        )
        ptd = dd.py_types_dict()
        assert ptd['myfield'] is str
