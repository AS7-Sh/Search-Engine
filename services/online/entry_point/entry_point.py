import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from pydantic.main import BaseModel

router = APIRouter()


class Query(BaseModel):
    query: str
    page: int
    dataset: str
    optimized: bool


class QueryRefinement(BaseModel):
    query: str
    dataset: str


@router.post("/search")
async def search(body: Query):
    get_inp_url = f"http://localhost:8000/query-representation"
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url,
                                     json={'query': body.query, 'dataset': body.dataset,
                                           'optimized': body.optimized},
                                     timeout=httpx.Timeout(100.0))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    get_inp_url = f"http://localhost:8000/query/match?page=" + \
                  str(body.page) + "&dataset=" + \
                  str(body.dataset) + "&optimized=" + \
                  str(body.optimized)
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url, json=response.json(), timeout=httpx.Timeout(100.0))

    return {'search_results': response.json()}


@router.post("/query-suggestion")
async def search(body: QueryRefinement):
    get_inp_url = f"http://localhost:8000/preprocess/spell-check"
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url,
                                     json={'query': body.query},
                                     timeout=httpx.Timeout(100.0))

    get_inp_url = f"http://localhost:8000/query-refinement"
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url,
                                     json={'query': response.json()['corrected'], 'dataset': body.dataset},
                                     timeout=httpx.Timeout(100.0))

    get_inp_url = f"http://localhost:8000/query/match?page=1" + \
                  "&dataset=" + \
                  str(body.dataset) + "&optimized=False"
    async with httpx.AsyncClient() as client:
        response = await client.post(get_inp_url, json=response.json(), timeout=httpx.Timeout(100.0))

    return {'search_results': response.json()}
