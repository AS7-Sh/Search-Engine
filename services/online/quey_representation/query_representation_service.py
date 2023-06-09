from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from services.online.quey_representation.query_representation import QueryRepresentation
import httpx

router = APIRouter()


class Query(BaseModel):
    query: str
    dataset: str
    optimized: bool


class QueryRefinement(BaseModel):
    query: str
    dataset: str


@router.post("/query-representation", name="query_representation")
async def query_representation(query_request: Query):
    if not query_request.optimized:
        get_inp_url = f"http://localhost:8000/preprocess/spell-check"
        async with httpx.AsyncClient() as client:
            response = await client.post(get_inp_url,
                                         json={'query': query_request.query},
                                         timeout=httpx.Timeout(100.0))

        return {
            'vector': pd.Series(
                QueryRepresentation.tfidf_vectorize_query(response.json()['corrected'], query_request.dataset)
            ).to_json(orient='values')
        }

    else:
        get_inp_url = f"http://localhost:8000/preprocess/spell-check"
        async with httpx.AsyncClient() as client:
            response = await client.post(get_inp_url,
                                         json={'query': query_request.query},
                                         timeout=httpx.Timeout(100.0))

        get_inp_url = f"http://localhost:8000/preprocess/clean_data"
        async with httpx.AsyncClient() as client:
            response = await client.post(get_inp_url, json={'query': response.json()['corrected']},
                                         timeout=httpx.Timeout(100.0)
                                         )

        get_inp_url = f"http://localhost:8000/preprocess/tokenize"
        async with httpx.AsyncClient() as client:
            response = await client.post(get_inp_url, json={'query': response.json()['cleaned_text']},
                                         timeout=httpx.Timeout(100.0)
                                         )

        return {
            'vector': pd.Series(
                QueryRepresentation.word_embedding_vectorize_query(
                    response.json()['tokens'], query_request.dataset
                )).to_json(orient='values')
        }


@router.post("/query-refinement", name="query_refinement")
async def query_representation(query_request: QueryRefinement):
    return {
        'vector': pd.Series(
            QueryRepresentation.tfidf_vectorize_query(query_request.query, query_request.dataset)
        ).to_json(orient='values')
    }
