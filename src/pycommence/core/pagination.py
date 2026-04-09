from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MoreAvailable:
    n_more: int

    def __bool__(self):
        return self.n_more > 0


@dataclass
class Pagination:
    offset: int = 0
    limit: int = 100

    def __bool__(self):
        return any([self.limit, self.offset])

    def __str__(self):
        return f'Pagination: offset={self.offset}, limit={self.limit or "None"}'

    def next_page(self):
        return Pagination(offset=self.offset + self.limit, limit=self.limit)

    def prev_page(self):
        return Pagination(offset=max(0, self.offset - self.limit), limit=self.limit)
