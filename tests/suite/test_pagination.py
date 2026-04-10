"""Tests for pycommence.core.pagination"""

from pycommence.core.pagination import MoreAvailable, Pagination


class TestPagination:
    def test_defaults(self):
        p = Pagination()
        assert p.offset == 0
        assert p.limit == 100

    def test_bool_truthy_with_limit(self):
        assert bool(Pagination(limit=10))

    def test_bool_truthy_with_offset(self):
        assert bool(Pagination(offset=5, limit=0))

    def test_str(self):
        s = str(Pagination(offset=10, limit=20))
        assert '10' in s and '20' in s

    def test_next_page(self):
        p = Pagination(offset=0, limit=50)
        nxt = p.next_page()
        assert nxt.offset == 50
        assert nxt.limit == 50

    def test_prev_page_clamps_to_zero(self):
        p = Pagination(offset=10, limit=50)
        prev = p.prev_page()
        assert prev.offset == 0

    def test_prev_page_normal(self):
        p = Pagination(offset=100, limit=50)
        prev = p.prev_page()
        assert prev.offset == 50


class TestMoreAvailable:
    def test_truthy(self):
        assert bool(MoreAvailable(n_more=5))

    def test_falsy(self):
        assert not bool(MoreAvailable(n_more=0))

    def test_negative_falsy(self):
        assert not bool(MoreAvailable(n_more=-1))
