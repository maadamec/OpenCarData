"""Class to store information from the EsaCar website"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class AaaCar:
    """ Class representing one car from AAA Auto without variable properties"""
    car_id: UUID
    url: str
    image: str
    aaa_id: str
    brand: str
    full_name: str
    engine: str
    equipment_class: (str | None)
    year: int
    gear: str
    power: int
    fuel: str
    body_type: (str | None)
    mileage: (int | None)
    datetime_captured: datetime
    datetime_sold: (datetime | None)
    job_id: (UUID | None)

@dataclass
class AaaCarVariable:
    car_variable_id: UUID
    car_id: UUID
    monthly_price: int
    special_price: int
    price: int
    discount: int
    datetime_captured: datetime
    job_id: (UUID | None)

@dataclass
class Job:
    """ Class to represent job run """
    job_id: int
    job_name: str
    datetime_start: datetime
    datetime_end: (datetime | None)
    detail: str
