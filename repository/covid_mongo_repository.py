import logging
from datetime import date, datetime, timezone
from typing import List, Union

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

    def get_records(
        self,
        iso_code: str,
        start: Union[date, None] = None,
        end: Union[date, None] = None,
    ):
        filter = {
            "iso_code": iso_code,
            "date": {},
        }

        if start:
            filter["date"]["$gte"] = datetime(
                start.year, start.month, start.day, 0, 0, 0, tzinfo=timezone.utc
            )

        if end:
            filter["date"]["$lte"] = datetime(
                end.year, end.month, end.day, 0, 0, 0, tzinfo=timezone.utc
            )

        project = {"new_cases": 1, "new_deaths": 1, "date": 1, "_id": 0}
        sort = list({"date": 1}.items())

        result = self.collection.find(filter=filter, projection=project, sort=sort)
        return list(result)