"""Class to store information from the EsaCar website"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EsaCar:
    """ Class representing one car from Auto ESA with variable properties """
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
    lowcost: bool
    premium: bool
    monthly_price: int
    special_price: int
    tags: list[str]
    condition: float
    price: int
    discount: int
    datetime_captured: datetime
    datetime_sold: (datetime | None)
