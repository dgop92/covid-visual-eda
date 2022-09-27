import logging
from typing import Optional

from pymongo import database

from repository.covid_mongo_repository import CovidRecordMongoRepository

logger = logging.getLogger(__name__)

covid_record_repository = None


def get_covid_record_repository(
    db: Optional[database.Database] = None,
) -> CovidRecordMongoRepository:
    global covid_record_repository
    logger.info("getting covid record repository")
    if covid_record_repository is None and db is not None:
        logger.info("creating covid record repository")
        covid_record_repository = CovidRecordMongoRepository(db)
    return covid_record_repository
