import logging
from typing import Any, Dict

import numpy as np
import pandas as pd

from config.database import get_mongo_database
from config.logging import config_logger
from entities.country import Country
from repository.country_mongo_repository import CountryMongoRepository

logger = logging.getLogger(__name__)

COUNTRY_DATA_PATH = "data/countries.csv"


def from_dict_to_country(d: Dict[str, Any]) -> Country:
    population = None if np.isnan(d["population"]) else d["population"]
    population_density = (
        None if np.isnan(d["population_density"]) else d["population_density"]
    )
    gdp_per_capita = None if np.isnan(d["gdp_per_capita"]) else d["gdp_per_capita"]
    return Country(
        iso_code=d["iso_code"],
        continent=d["continent"],
        name=d["location"],
        population=population,
        population_density=population_density,
        gdp_per_capita=gdp_per_capita,
    )


def save_countries(repository: CountryMongoRepository):
    logger.info("reading countries from csv")
    country_df = pd.read_csv(COUNTRY_DATA_PATH)
    raw_countries = country_df.reset_index().to_dict("records")
    logger.info("converting raw countries dicts to country entities")
    countries = [from_dict_to_country(d) for d in raw_countries]
    repository.bulk_create(countries)
    logger.info("countries saved successfully")


if __name__ == "__main__":
    config_logger()

    logger.info("connecting to mongo database")
    db = get_mongo_database()
    repository = CountryMongoRepository(db)
    logger.info("connected to mongo database")

    save_countries(repository)
