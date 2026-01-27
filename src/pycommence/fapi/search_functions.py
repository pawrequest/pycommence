"""
Module for backend integration with PyCommence data sources.

Provides async functions for querying, fetching, and searching records
using PyCommence, with support for pagination and filtering.
"""

from __future__ import annotations

from fastapi import Depends
from loguru import logger

from pycommence.fapi.depends import pycmc_f_query
from pycommence.fapi.search_request_response import MoreAvailableFront, SearchRequest, SearchResponse
from pycommence.filters import FieldFilter, FilterArray
from pycommence.meta.meta import get_table_type
from pycommence import MoreAvailable, PyCommence
from pycommence.rows import RowData


async def pycommence_fetch(
        q: SearchRequest = Depends(SearchRequest.from_query),
        pycmc: PyCommence = Depends(pycmc_f_query),
) -> RowData:
    q.max_rtn = 1
    if not q.row_id:
        logger.debug(f'Getting row_id for pk_value: {q.pk_value} in csr: {q.csrname}')
        pval = q.pk_value
        pval = pval.strip('"')
        q.row_id = pycmc.csr(q.csrname).pk_to_id(pval)
    row: RowData = pycmc.read_row(csrname=q.csrname, row_id=q.row_id)
    return row


async def pycommence_search(
        q: SearchRequest = Depends(SearchRequest.from_query),
        pycmc: PyCommence = Depends(pycmc_f_query),
) -> SearchResponse:
    table_type = get_table_type(q.csrname, mode='all', missing='raise')
    filter_array = FilterArray.from_filters(
        FieldFilter(column=table_type.pk_key, condition=q.condition, value=q.pk_value) if q.pk_value else None
    )
    records, more = await pycommence_gather(pycmc=pycmc, q=q, filter_array=filter_array)
    return SearchResponse(records=records, more=more, search_request=q)


async def pycommence_gather(
        pycmc: PyCommence,
        q: SearchRequest,
        filter_array: FilterArray | None = None,
) -> tuple[list[RowData], MoreAvailable | None]:
    """
    Gather records from PyCommence based on the provided search request.
    Add MoreAvailable if q has pagination and there are more records to fetch.
    """

    logger.debug('Gathering records from PyCommence')
    more = None
    records = []
    for row in pycmc.read_rows(csrname=q.csrname, pagination=q.pagination, filter_array=filter_array):
        if isinstance(row, MoreAvailable):
            more = MoreAvailableFront(n_more=row.n_more, json_link=q.next_q_str_json, html_link=q.next_q_str)
            break
        records.append(row)
    return records, more
