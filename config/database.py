from pymongo import MongoClient, database

from config.settings import DATABASE


def get_mongo_database() -> database.Database:
    client = MongoClient(DATABASE["mongo_url"])
    return client[DATABASE["db_name"]]
