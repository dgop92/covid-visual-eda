from decouple import config
from pymongo import MongoClient, database


def get_mongo_database() -> database.Database:
    MONGO_URL = config("MONGO_URL")
    DB_NAME = config("DB_NAME")

    client = MongoClient(MONGO_URL)
    return client[DB_NAME]
