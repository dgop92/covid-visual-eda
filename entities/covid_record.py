from datetime import datetime

from pydantic import BaseModel


class CovidRecord(BaseModel):
    iso_code: str
    date: datetime
    total_cases: int
    new_cases: int
    total_deaths: int
    new_deaths: int
