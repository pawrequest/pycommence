"""Tests for pycommence.log_config"""

from pycommence.log_config import coloured, configure_loguru


class TestColoured:
    def test_wraps_in_tags(self):
        result = coloured('hello', 'red')
        assert result == '<red>hello</red>'


class TestConfigureLoguru:
    def test_does_not_raise(self):
        configure_loguru(level='WARNING')
