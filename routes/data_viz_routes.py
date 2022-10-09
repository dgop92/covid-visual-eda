from datetime import date
from typing import Union

from fastapi import APIRouter

from repository.factories import get_covid_record_repository

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


@data_viz_router.get("/south-america-stringency-index")
def get_south_america_stringency_index(
    start: Union[date, None] = None,
    end: Union[date, None] = None,
):
    if not start:
        start = date(2020, 1, 1)

    if not end:
        end = date(2020, 12, 31)

    repository = get_covid_record_repository()
    results = repository.get_south_america_stringency_index(start, end)
    return results


@data_viz_router.get("/countries-basic-info")
def countries_basic_info(
    start: Union[date, None] = None,
    end: Union[date, None] = None,
):
    if not start:
        start = date(2020, 1, 1)

    if not end:
        end = date(2020, 12, 31)

    repository = get_covid_record_repository()
    results = repository.get_countries_basic_info(start, end)
    return results
