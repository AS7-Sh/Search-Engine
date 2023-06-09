from fastapi import FastAPI
from xlwings.quickstart_fastapi.main import app
from fastapi.middleware.cors import CORSMiddleware

from services.online.query_matching.query_matching_ranking_service import router as query_matching_ranking_router
from services.online.entry_point.entry_point import router as entry_point
from services.online.quey_representation.query_representation_service import router as query_representation_router
from services.text_processing.data_preprocessing_service import router as data_preprocessing_router
from utils.files_handling.files_handler import FilesHandler

fast_app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_representation_router, tags=["Query Representation"])
app.include_router(query_matching_ranking_router, tags=["Query Matching and Ranking"])
app.include_router(data_preprocessing_router, tags=["Data Preprocessing"])
app.include_router(entry_point, tags=["Entry point"])

