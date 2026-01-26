from __future__ import annotations

from typing import Self

from fastapi import Depends, Query
from pydantic import BaseModel, Field

from pycommence.filters import ConditionType
from pycommence.pagination import Pagination as _Pagination

PAGE_SIZE = 50


async def get_condition(condition: str = Query('')) -> ConditionType:
    return getattr(ConditionType, condition.upper(), ConditionType.CONTAIN)


class Pagination(_Pagination):
    @classmethod
    def from_query(cls, limit: int = Query(PAGE_SIZE), offset: int = Query(0)) -> Self:
        return cls(limit=limit, offset=offset)


class SearchRequest(BaseModel):
    csrname: str | None = None
    row_id: str | None = None
    pk_value: str | None = None
    condition: ConditionType = ConditionType.CONTAIN
    max_rtn: int | None = None
    pagination: Pagination | None = Pagination()
    cmc_filter_i: int = 0
    py_filter_i: int = 0


    def __str__(self):
        return (
            f'Csr: {self.csrname}'
            f'{' | pk=:' + self.pk_value if self.pk_value else ''}'
            f'{' | row_id=:' + self.row_id if self.row_id else ''}'
            f'{' | customer_name="' + self.customer_name + '"' if self.customer_name else ''}'
            f'{' | cmc_filter_i=' + str(self.cmc_filter_i) if self.cmc_filter_i else ''}'
            f'{' | py_filter_i=' + str(self.py_filter_i) if self.py_filter_i else ''}'
            f'{' | ' + str(self.pagination) if self.pagination else ''}'
        )

    @property
    def q_str(self):
        return self.q_str_paginate()

    @property
    def query_str_json(self):
        return self.q_str_paginate(api=True)

    @property
    def next_q_str(self):
        return self.q_str_paginate(self.pagination.next_page()) if self.pagination else None

    @property
    def next_q_str_json(self):
        return self.q_str_paginate(self.pagination.next_page(), api=True) if self.pagination else None

    def q_str_paginate(self, pagination: Pagination = None, api: bool = False):
        pagination = pagination or self.pagination
        qstr = '/api' if api else ''
        qstr += f'/search?csrname={self.csrname}'
        for attr in [
            'condition',
            'max_rtn',
            'cmc_filter_i',
            'py_filter_i',
            'pk_value',
            'row_id',
            'customer_name',
        ]:
            if val := getattr(self, attr):
                qstr += f'&{attr}={val}'
        if pagination:
            if pagination.limit:
                qstr += f'&limit={pagination.limit}'
            if pagination.offset:
                qstr += f'&offset={pagination.offset}'
        return qstr

    def next_request(self):
        return self.model_copy(update={'pagination': self.pagination.next_page()})

    def prev_request(self):
        return self.model_copy(update={'pagination': self.pagination.prev_page()})

    @classmethod
    def from_query(
            cls,
            csrname: str = Query(None),
            pk_value: str = Query(''),
            pagination: Pagination = Depends(Pagination.from_query),
            condition: ConditionType = Depends(get_condition),
            max_rtn: int = Query(None),
            row_id: str = Query(None),
            customer_name: str = Query(None),
            py_filter_i: int = Query(0),
            cmc_filter_i: int = Query(0),
    ):
        return cls(
            csrname=csrname,
            pagination=pagination,
            pk_value=pk_value,
            condition=condition,
            max_rtn=max_rtn,
            row_id=row_id,
            customer_name=customer_name,
            cmc_filter_i=cmc_filter_i,
            py_filter_i=py_filter_i,
        )
