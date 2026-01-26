from __future__ import annotations

from typing import Sequence

from pydantic import BaseModel, model_validator

from pycommence import MoreAvailable
from pycommence.fapi.search_request import SearchRequest
from pycommence.meta.meta import CommenceTable, CommenceRecord


class SearchResponse[T: CommenceTable](BaseModel):
    records: list[T]
    length: int = 0
    search_request: SearchRequest
    more: MoreAvailable | None = None

    def __str__(self):
        return (
            f'Search Response: {self.length}x {self.search_request.csrname if self.search_request.csrname else ', '.join(self.search_request.csrnames)} records'
            f'{' (' + str(self.more.n_more) + ' more available),' if self.more else '. '} '
            f'SearchRequest[{str(self.search_request)}]'
        )

    @model_validator(mode='after')
    def set_length(self):
        self.length = len(self.records)
        return self


class SearchResponseMulti(SearchResponse):
    search_request: Sequence[SearchRequest]

    def __str__(self):
        rtypes = '/'.join([req.csrname for req in self.search_request])
        return (
            f'Search Response with {self.length}x {rtypes} records. '
            f'SearchRequests[{'; '.join(str(_) for _ in self.search_request)}]'
            f'{', ' + str(self.more.n_more) + ' more available' if self.more else ''} '
        )
