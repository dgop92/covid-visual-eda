import logging
from typing import List

import pandas as pd

from config.logging import config_logger

logger = logging.getLogger(__name__)

COVID_DATA_PATH = "data/owid-covid-data.csv"
COUNTRY_DATA_PATH = "data/countries.csv"

RECORD_TEMPLATE_PATH = "data/country_covid_records/{iso_code}_covid_records.csv"
COVID_RECORDS_COLUMNS = [
    "date",
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
]


def get_country_covid_records_from_df(
    param_df: pd.DataFrame, iso_code: str
) -> pd.DataFrame:

    df = param_df[param_df["iso_code"] == iso_code]
    return df[COVID_RECORDS_COLUMNS]


def create_country_covid_records(iso_codes: List[str]):

    for iso_code in iso_codes:
        logger.info(f"processing iso code: {iso_code}")
        logger.info("reading covid data by chunks")
        record_dfs = []
        fileiterator = pd.read_csv(COVID_DATA_PATH, chunksize=10000)
        for chunk_df in fileiterator:
            logger.info("processing chunk...")
            curent_record_df = get_country_covid_records_from_df(chunk_df, iso_code)
            # records are sorted by acessing iso_code,
            # so if no records are found and we already have some records, we can stop
            if curent_record_df.empty and len(record_dfs) != 0:
                break

            if not curent_record_df.empty:
                record_dfs.append(curent_record_df)

        logger.info("closing covid data file")
        fileiterator.close()
        logger.info("concatenating records")
        records_df = pd.concat(record_dfs)
        logger.info("writing records to file")
        records_df.to_csv(RECORD_TEMPLATE_PATH.format(iso_code=iso_code), index=False)


if __name__ == "__main__":
    config_logger()

    logger.info("retrieve country iso codes")
    countries_df = pd.read_csv(COUNTRY_DATA_PATH, index_col=0)
    all_iso_codes = countries_df.index.values
    logger.info(f"found {len(all_iso_codes)} iso codes")

    logger.info("creating country records")
    create_country_covid_records(all_iso_codes)
