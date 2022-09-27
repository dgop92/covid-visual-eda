from datetime import date
from typing import Union

from fastapi import APIRouter

from repository.factories import get_covid_record_repository

data_viz_router = APIRouter()


@data_viz_router.get("/")
async def index():
    return {"message": "Hello World!"}


@data_viz_router.get("/covid-records/{iso_code}")
def get_covid_records(
    iso_code: str,
    start: Union[date, None] = None,
    end: Union[date, None] = None,
):
    repository = get_covid_record_repository()
    return repository.get_records(iso_code, start, end)


@data_viz_router.get("/total-cases-population")
def get_total_cases_with_country_population():
    repository = get_covid_record_repository()
    return repository.get_total_cases_with_country_population()
