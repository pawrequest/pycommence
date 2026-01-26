"""
Module for backend integration with PyCommence data sources.

Provides async functions for querying, fetching, and searching records
using PyCommence, with support for pagination and filtering.
"""

from __future__ import annotations

import dataclasses

from fastapi import Depends
from loguru import logger

from pycommence.fapi.depends import pycmc_f_query
from pycommence.fapi.search_response import SearchResponse
from pycommence.fapi.search_request import SearchRequest
from pycommence.filters import FieldFilter, FilterArray
from pycommence.meta.meta import CommenceTable, get_table_type
from pycommence import MoreAvailable, PyCommence


async def pycommence_gather(
        pycmc: PyCommence,
        q: SearchRequest,
        filter_array: FilterArray | None = None,
) -> tuple[list[CommenceTable], MoreAvailable | None]:
    """
    Gather records from PyCommence based on the provided search request.
    Add MoreAvailable if q has pagination and there are more records to fetch.
    """

    logger.debug('GATHERING')
    more = None
    records = []
    for row in pycmc.read_rows(csrname=q.csrname, pagination=q.pagination, filter_array=filter_array):
        if isinstance(row, MoreAvailable):
            more = MoreAvailableFront(n_more=row.n_more, json_link=q.next_q_str_json, html_link=q.next_q_str)
            break
        records.append(row)
    return records, more



async def pycommence_search[T:CommenceTable](
        q: SearchRequest = Depends(SearchRequest.from_query),
        pycmc: PyCommence = Depends(pycmc_f_query),
) -> SearchResponse[T]:
    table_type:type[T] = get_table_type(q.csrname)
    cmc_filter = FieldFilter(column=table_type.pk_key, condition=q.condition, value=q.pk_value) if q.pk_value else None
    filter_array = FilterArray.from_filters(cmc_filter)
    records, more = await pycommence_gather(pycmc=pycmc, q=q, filter_array=filter_array)
    resp = SearchResponse(records=records, more=more, search_request=q)
    return resp


async def pycommence_get_one(
        q: SearchRequest = Depends(SearchRequest.from_query),
        pycmc: PyCommence = Depends(pycmc_f_query),
) -> CommenceTable:
    q.max_rtn = 1
    if not q.row_id:
        logger.debug(f'Getting row_id for pk_value: {q.pk_value} in csr: {q.csrname}')
        pval = q.pk_value
        if pval.startswith('"') and pval.endswith('"'):
            pval = pval[1:-1]
        q.row_id = pycmc.csr(q.csrname).pk_to_id(pval)
    return pycmc.read_row2(csrname=q.csrname, row_id=q.row_id)


@dataclasses.dataclass
class MoreAvailableFront(MoreAvailable):
    json_link: str = None
    html_link: str = None
