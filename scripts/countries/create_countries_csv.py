import logging

import pandas as pd

from config.logging import config_logger

logger = logging.getLogger(__name__)

COUNTRY_COLUMNS = [
    "iso_code",
    "continent",
    "location",
    "population",
    "population_density",
    "gdp_per_capita",
    "life_expectancy",
    "stringency_index",
    "human_development_index",
]
DROP_DUPLICATES_COLUMNS = ["iso_code", "continent", "location"]
COVID_DATA_PATH = "data/owid-covid-data.csv"
COUNTRY_DATA_PATH = "data/countries.csv"


def get_country_dataframe():
    country_dfs = []

    logger.info("reading covid data by chunks")

    fileiterator = pd.read_csv(COVID_DATA_PATH, chunksize=10000)
    for chunk_df in fileiterator:
        logger.info("processing chunk...")
        curr_country_info_df = chunk_df[COUNTRY_COLUMNS]
        curr_country_info_df = curr_country_info_df.drop_duplicates(
            subset=DROP_DUPLICATES_COLUMNS
        )
        country_dfs.append(curr_country_info_df)

    logger.info("concatenating dataframes")
    country_df = pd.concat(country_dfs)
    logger.info("removing anormal iso codes")
    country_df_no_owid = country_df[~country_df["iso_code"].str.contains("OWID")]
    logger.info("removing duplicates")
    country_df_no_duplicates = country_df_no_owid.drop_duplicates(
        subset=DROP_DUPLICATES_COLUMNS
    )
    return country_df_no_duplicates.set_index("iso_code")


if __name__ == "__main__":
    config_logger()
    country_df = get_country_dataframe()
    logger.info("writing to csv")
    country_df.to_csv(COUNTRY_DATA_PATH)
