from fastapi import APIRouter
from services.text_processing.data_preprocessing import TextPreprocessor
from pydantic import BaseModel
from services.text_processing.spell_checking import correct_data_spelling

router = APIRouter()


class Query(BaseModel):
    query: str


@router.post("/preprocess/clean_data")
async def preprocess_text(query_request: Query):
    return {'cleaned_text': TextPreprocessor().preprocess(query_request.query)}


@router.post("/preprocess/tokenize")
async def tokenize_text(query_request: Query):
    return {'tokens': TextPreprocessor().tokenize(query_request.query)}


@router.post("/preprocess/spell-check")
async def tokenize_text(query_request: Query):
    return {'corrected': correct_data_spelling(query_request.query)}
