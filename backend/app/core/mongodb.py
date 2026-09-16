from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

from backend.app.core.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    settings = get_settings()

    return MongoClient(
        host=settings.mongo_host,
        port=settings.mongo_port,
        serverSelectionTimeoutMS=5000,
    )


def get_mongo_database() -> Database:
    settings = get_settings()

    return get_mongo_client()[settings.mongo_db]