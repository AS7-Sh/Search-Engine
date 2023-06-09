from xlwings.quickstart_fastapi.main import app
from pymongo import MongoClient

MONGO_URI = "localhost:27017"


def get_mongo_client():
    client = MongoClient(MONGO_URI)
    return client


@app.on_event("startup")
async def startup_event():
    app.mongodb_client = get_mongo_client()


@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
