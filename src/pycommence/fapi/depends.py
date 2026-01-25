from typing import Self

from fastapi import Query
from pydantic import BaseModel

from pycommence import pycommence_context
from pycommence.pycmc_types import Pagination as _Pagination

PAGE_SIZE: int = 50


class Pagination(_Pagination):
    @classmethod
    def from_query(cls, limit: int = Query(PAGE_SIZE), offset: int = Query(0)) -> Self:
        return cls(limit=limit, offset=offset)


class SearchRequest(BaseModel):
    csrname: str | None = None
    row_id: str | None = None
    pk_value: str | None = None
    max_rtn: int | None = None
    pagination: Pagination | None = Pagination()

    @classmethod
    def from_query(
            cls,
            csrname: str = Query(...),
            row_id: str = Query(None),
            pk_value: str = Query(None),
            max_rtn: int = Query(None),
            limit: int = Query(PAGE_SIZE),
            offset: int = Query(0),
    ) -> Self:
        pagination = Pagination(limit=limit, offset=offset)
        return cls(
            csrname=csrname,
            row_id=row_id,
            pk_value=pk_value,
            max_rtn=max_rtn,
            pagination=pagination,
        )

async def pycmc_f_query(csrname: str = Query(...)):
    with pycommence_context(csrname=csrname) as pycmc:
        yield pycmc
