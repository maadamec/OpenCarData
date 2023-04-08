"""Class to store information from the EsaCar website"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CarDto:
    """ Class representing one car from AUTO ESA without variable attributes """
    car_id: (int | None)
    url: str
    image: str
    esa_id: str
    brand: str
    full_name: str
    engine: str
    equipment_class: str
    year: int
    gear: str
    power: int
    fuel: str
    body_type: str
    mileage: int
    tags: list[str]
    datetime_captured: datetime
    datetime_sold: (datetime | None)
    job_id: (int | None)
