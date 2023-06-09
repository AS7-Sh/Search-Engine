import json

from fastapi import APIRouter
from services.online.query_matching.query_matching_ranking import QueryMatchingRanking
from pydantic import BaseModel

router = APIRouter()


class Query(BaseModel):
    vector: str


@router.post("/query/match")
async def search(page: int, dataset: str, optimized: bool, body: Query):
    if not optimized:
        return {
            'search_results': QueryMatchingRanking(page, 10, 0.35).get_tfidf_results(dataset, [json.loads(body.vector)])
        }

    else:

        return {
            'search_results': QueryMatchingRanking(page, 20, 0.35).get_word_embedding_results(dataset,
                                                                                              [json.loads(body.vector)])
        }
