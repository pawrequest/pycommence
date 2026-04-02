from pycommence.core.row_data import RowData2
from pycommence.fapi.search_functions import pycommence_fetch, pycommence_search
from pycommence.fapi.search_request_response import SearchRequest, SearchResponse

try:
    from fastapi import APIRouter, Depends, Query
except ImportError:
    raise ImportError('FastAPI is not installed.')

router = APIRouter()


@router.get('/status')
async def get_status():
    return {'status': 'ok'}


@router.get('/search')
async def pycommence_search_endpoint(
    q: SearchRequest = Depends(SearchRequest.from_query), auto_model: bool = Query(False)
) -> SearchResponse:
    search_response = await pycommence_search(q=q, auto_model=auto_model)
    return search_response


# @router.get('/search1')
# async def pycommence_search_endpoint1(
#         search_response: SearchResponse = Depends(pycommence_search),
#
# ) -> SearchResponse:
#     return search_response


@router.get('/get')
async def pycommence_get_endpoint(
    q: SearchRequest = Depends(SearchRequest.from_query),
) -> RowData2:
    record = await pycommence_fetch(q=q)
    return record
