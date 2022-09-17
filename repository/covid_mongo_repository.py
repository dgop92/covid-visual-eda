import logging
from typing import List

from pymongo import database

from entities.covid_record import CovidRecord

logger = logging.getLogger(__name__)


class CovidRecordMongoRepository:
    def __init__(self, db: database.Database) -> None:
        logger.info("initializing covid record mongo repository")
        self.collection = db["covid_records"]

    def bulk_create(self, covid_records: List[CovidRecord]):
        logger.info("saving all covid records in mongo repository")
        self.collection.insert_many([c.dict() for c in covid_records])
