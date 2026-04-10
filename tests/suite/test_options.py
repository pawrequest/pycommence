"""Tests for pycommence.pycommence_options"""

from pycommence.pycommence_options import Options, get_options


class TestOptionsDefaults:
    def test_default_delim(self):
        assert Options().delim == ';*;%'

    def test_default_application_name(self):
        assert Options().application_name == 'Commence'

    def test_default_application_db_name(self):
        assert Options().application_db_name == 'Commence.DB'

    def test_default_strip_strs_false(self):
        assert Options().strip_strs is False

    def test_default_split_str_lists_true(self):
        assert Options().split_str_lists is True

    def test_default_max_cmd_len(self):
        assert Options().max_cmd_len == 256

    def test_default_fields_chunk(self):
        assert Options().fields_chunk == 12

    def test_default_generate_models_false(self):
        assert Options().generate_models is False


class TestOptionsCustom:
    def test_custom_delim(self):
        assert Options(delim='||').delim == '||'

    def test_custom_max_cmd_len(self):
        assert Options(max_cmd_len=512).max_cmd_len == 512


class TestGetOptions:
    def test_returns_options(self):
        assert isinstance(get_options(), Options)

    def test_cached(self):
        assert get_options() is get_options()
