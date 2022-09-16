from typing import Optional

from pydantic import BaseModel


class Country(BaseModel):
    iso_code: str
    name: str
    continent: str
    population_density: Optional[float]
    population: Optional[float]
    gdp_per_capita: Optional[float]
