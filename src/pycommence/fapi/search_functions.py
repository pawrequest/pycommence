"""
Module for backend integration with PyCommence data sources.

Provides async functions for querying, fetching, and searching records
using PyCommence, with support for pagination and filtering.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends, Query
from loguru import logger

from pycommence import MoreAvailable
from pycommence.conversation import get_or_create_table_type
from pycommence.core.filters import FieldFilter, FilterArray
from pycommence.core.meta import get_table_type
from pycommence.core.row_data import RowData
from pycommence.core.utils import alias_lookup
from pycommence.dde import DDETopic
from pycommence.fapi.search_request_response import MoreAvailableFront, SearchRequest, SearchResponse
from pycommence.pycommence_client import PyCommence


async def pycommence_fetch(
    q: SearchRequest = Depends(SearchRequest.from_query),
    auto_model=False,
) -> RowData:
    q.max_rtn = 1
    with PyCommence() as pycmc:
        csr = pycmc.cursor(q.csrname)
        if not q.row_id:
            logger.debug(f'Getting row_id for pk_value: {q.pk_value} in csr: {q.csrname}')
            pval = q.pk_value
            pval = pval.strip('"')
            q.row_id = q.row_id or csr.pk_to_id(pval)
        row: RowData = csr.read_row(row_id=q.row_id)
    return row


async def pycommence_search(
    q: SearchRequest,
    auto_model: bool = False,
) -> SearchResponse:
    with PyCommence() as pycmc:
        if auto_model:
            table_type = get_or_create_table_type(
                pycmc.conversation(DDETopic.GET),
                q.csrname,
            )
        else:
            table_type = get_table_type(q.csrname, mode='manual', missing='raise')
        if not table_type:
            raise ValueError(f'Unknown table type for csrname: {q.csrname}')
        col = pycmc.cursor(q.csrname).pk_label
        filter_array = FilterArray.from_filters(
            FieldFilter(column=col, condition=q.condition, value=q.pk_value)
            # FieldFilter(column=alias_lookup(table_type, 'firstName'), condition=q.condition, value=q.pk_value)
        )
        records, more = await pycommence_gather(pycmc=pycmc, q=q, filter_array=filter_array)
        return SearchResponse(records=records, more=more, search_request=q)


async def pycmc_f_query(
    csrname: str = Query(...),
) -> AsyncGenerator[PyCommence]:
    with PyCommence(csrname) as pycmc:
        yield pycmc


# async def pycommence_search1(
#         q: SearchRequest = Depends(SearchRequest.from_query),
#         auto_model: bool = False,
# ) -> SearchResponse:
#     with PyCommenceClient() as pycmc:
#         table_type = get_table_type(q.csrname)
#         if auto_model and table_type is None:
#             table_type = get_or_create_table_type(pycmc.conversation(DDETopic.GET), q.csrname)
#         filter_array = FilterArray.from_filters(
#             FieldFilter(column=table_type.name_field, condition=q.condition, value=q.pk_value) if q.pk_value else None
#         )
#         records, more = await pycommence_gather(pycmc=pycmc, q=q, filter_array=filter_array)
#         return SearchResponse(records=records, more=more, search_request=q)


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

    for row in pycmc.cursor(q.csrname).read_rows(pagination=q.pagination, filter_array=filter_array):
        if isinstance(row, MoreAvailable):
            more = MoreAvailableFront(n_more=row.n_more, json_link=q.next_q_str_json, html_link=q.next_q_str)
            break
        records.append(row)
    return records, more
