from pycommence.fapi.search_functions import pycommence_get_one, pycommence_search
from pycommence.fapi.search_response import SearchResponse
from pycommence.meta.meta import CommenceTable

try:
    from fastapi import APIRouter, Depends
except ImportError:
    raise ImportError("FastAPI is not installed.")

router = APIRouter()


@router.get("/status")
async def get_status():
    return {"status": "ok"}


@router.get('/search')
async def pycommence_search_endpoint(
        search_response: SearchResponse = Depends(pycommence_search),
) -> SearchResponse:
    return search_response


@router.get('/get')
async def pycommence_search_endpoint[T:CommenceTable](
        record: T = Depends(pycommence_get_one),
) -> T:
    return record
