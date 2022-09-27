import logging
from typing import List

from pymongo import database

from entities.country import Country

logger = logging.getLogger(__name__)


class CountryMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing country mongo repository")
        self.collection = db["countries"]

    def bulk_create(self, countries: List[Country]):
        self.collection.insert_many([country.dict() for country in countries])

    def delete_all(self):
        self.collection.delete_many({})
