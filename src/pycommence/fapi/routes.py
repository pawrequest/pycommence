from pycommence.fapi.search_functions import pycommence_search
from pycommence.fapi.search_response import SearchResponse

try:
    from fastapi import APIRouter, Depends
except ImportError:
    raise ImportError("FastAPI is not installed.")

router = APIRouter()


@router.get("/status")
async def get_status():
    return {"status": "ok"}


@router.get('/')
async def pycommence_search_endpoint(
    search_response: SearchResponse = Depends(pycommence_search),
) -> SearchResponse:
     return search_response


