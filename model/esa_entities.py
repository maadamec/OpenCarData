"""Class to store information from the EsaCar website"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class EsaCar:
    """ Class representing one car from Auto ESA without variable properties """
    car_id: UUID
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
    datetime_captured: datetime
    datetime_sold: (datetime | None)
    job_id: (UUID | None)


@dataclass
class EsaCarVariable:
    car_variable_id: UUID
    car_id: UUID
    lowcost: bool
    premium: bool
    monthly_price: int
    special_price: int
    condition: float
    price: int
    discount: int
    datetime_captured: datetime
    job_id: (UUID | None)
