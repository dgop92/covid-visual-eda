from datetime import date
from typing import Dict, Union

from fastapi import APIRouter

from repository.factories import get_covid_record_repository
from utils.helpers import get_mean, get_standard_deviation, get_z_score

data_viz_router = APIRouter()


@data_viz_router.get("/")
async def index():
    return {"message": "Hello World!"}


@data_viz_router.get("/covid-records/{iso_code}")
def covid_records(
    iso_code: str,
    start: Union[date, None] = None,
    end: Union[date, None] = None,
):
    repository = get_covid_record_repository()
    return repository.get_records(iso_code, start, end)


def country_record_is_not_outliner(
    property_name: str, data: Dict[str, any], mean: float, std: float
):
    z_score = get_z_score(mean, std, data[property_name])
    return z_score < 3


def is_country_record_valid(data):
    return bool(data["population_density"]) and bool(data["total_cases"])


@data_viz_router.get("/countries-basic-info")
def countries_basic_info(
    remove_outliers: bool = False,
    start: Union[date, None] = None,
    end: Union[date, None] = None,
):
    if not start:
        start = date(2020, 1, 1)

    if not end:
        end = date(2020, 12, 31)

    repository = get_covid_record_repository()
    results = repository.get_countries_basic_info(start, end)
    if remove_outliers:
        valid_results = [
            result for result in results if is_country_record_valid(result)
        ]
        pop_density_data = list(map(lambda d: d["population_density"], valid_results))
        total_cases_data = list(map(lambda d: d["total_cases"], valid_results))
        mean_pop_density = get_mean(pop_density_data)
        mean_total_cases = get_mean(total_cases_data)
        std_pop_density = get_standard_deviation(pop_density_data, mean_pop_density)
        std_total_cases = get_standard_deviation(total_cases_data, mean_total_cases)
        results = list(
            filter(
                lambda d: country_record_is_not_outliner(
                    "population_density", d, mean_pop_density, std_pop_density
                )
                and country_record_is_not_outliner(
                    "total_cases", d, mean_total_cases, std_total_cases
                ),
                valid_results,
            )
        )
    return results
