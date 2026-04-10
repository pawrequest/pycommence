"""Tests for pycommence.icommence.const"""

from pycommence.icommence.const import (
    CursorType,
    OptionFlag,
    SeekBookmark,
)


class TestCursorType:
    def test_category(self):
        assert CursorType.CATEGORY == 0

    def test_view(self):
        assert CursorType.VIEW == 1


class TestOptionFlag:
    def test_none(self):
        assert OptionFlag.NONE == 0

    def test_canonical(self):
        assert OptionFlag.CANONICAL == 0x0010

    def test_combinable(self):
        combined = OptionFlag.FIELD_NAME | OptionFlag.CANONICAL
        assert combined == 0x0011


class TestSeekBookmark:
    def test_beginning(self):
        assert SeekBookmark.BEGINNING.value == 0

    def test_current(self):
        assert SeekBookmark.CURRENT.value == 1

    def test_end(self):
        assert SeekBookmark.END.value == 2
