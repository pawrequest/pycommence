from fastapi import Query

from pycommence import pycommence_context


async def pycmc_f_query(csrname: str = Query(...)):
    with pycommence_context(csrname) as pycmc:
        yield pycmc


async def pycmc_f_query_multi_csr(csrnames: list[str] = Query(...)):
    with pycommence_context(*csrnames) as pycmc:
        yield pycmc
