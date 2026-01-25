from pycommence import PyCommence
from pycommence.exceptions import PyCommenceMaxExceededError, PyCommenceNotFoundError
from pycommence.fapi.depends import SearchRequest, pycmc_f_query

try:
    from fastapi import APIRouter, Depends
except ImportError:
    raise ImportError("FastAPI is not installed.")

router = APIRouter()


@router.get("/status")
async def get_status():
    return {"status": "ok"}


@router.get("/search_csr", response_model=dict[str, str])
async def get_item(
        search_request: SearchRequest = Depends(SearchRequest.from_query),
        pycmc: PyCommence = Depends(pycmc_f_query)
) -> dict[str, str]:
    try:
        res = pycmc.read_row(pk=search_request.pk_value)
        return res.data
    except PyCommenceNotFoundError:
        return {"error": "Record not found"}
    except PyCommenceMaxExceededError:
        return {"error": "Maximum records exceeded"}
