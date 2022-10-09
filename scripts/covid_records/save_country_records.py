import logging
from typing import Any, Dict, List

import pandas as pd

from config.database import get_mongo_database
from config.logging import config_logger
from entities.covid_record import CovidRecord
from repository.covid_mongo_repository import CovidRecordMongoRepository

logger = logging.getLogger(__name__)

COUNTRY_DATA_PATH = "data/countries.csv"

RECORD_TEMPLATE_PATH = "data/country_covid_records/{iso_code}_covid_records.csv"
COVID_RECORDS_COLUMNS = [
    "date",
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
]


def from_dict_to_covid_record(d: Dict[str, Any]) -> CovidRecord:
    return CovidRecord(
        iso_code=d["iso_code"],
        date=d["date"].to_pydatetime(),
        total_cases=d["total_cases"],
        new_cases=d["new_cases"],
        total_deaths=d["total_deaths"],
        new_deaths=d["new_deaths"],
        stringency_index=d["stringency_index"],
    )


def save_country_covid_record(iso_code: str, repository: CovidRecordMongoRepository):
    country_records_df = pd.read_csv(
        RECORD_TEMPLATE_PATH.format(iso_code=iso_code), parse_dates=["date"]
    )

    # Cleaning the data
    country_records_df[["new_cases", "new_deaths"]] = country_records_df[
        ["new_cases", "new_deaths"]
    ].fillna(0)
    country_records_df[["total_cases", "total_deaths"]] = (
        country_records_df[["new_cases", "new_deaths"]]
        .fillna(method="ffill")
        .fillna(method="bfill")
    )
    country_records_df["stringency_index"] = (
        country_records_df["stringency_index"]
        .fillna(method="ffill")
        .fillna(method="bfill")
    )

    raw_records = country_records_df.to_dict("records")
    covid_records = [from_dict_to_covid_record(d) for d in raw_records]
    repository.bulk_create(covid_records)


def save_country_covid_records(
    iso_codes: List[str], repository: CovidRecordMongoRepository
):
    for iso_code in iso_codes:
        try:
            logger.info(f"saving covid records for country {iso_code}")
            save_country_covid_record(iso_code, repository)
            logger.info(f"covid records for country {iso_code} successfully saved")
        except Exception as e:
            logger.error(f"error saving covid records for country {iso_code}")
            logger.error(e)


if __name__ == "__main__":
    config_logger()

    logger.info("retrieve country iso codes")
    countries_df = pd.read_csv(COUNTRY_DATA_PATH, index_col=0)
    all_iso_codes = countries_df.index.values
    logger.info(f"found {len(all_iso_codes)} iso codes")

    logger.info("connecting to mongo database")
    db = get_mongo_database()
    repository = CovidRecordMongoRepository(db)
    logger.info("connected to mongo database")

    logger.info("delete all covid records")
    repository.delete_all()

    save_country_covid_records(all_iso_codes, repository)
