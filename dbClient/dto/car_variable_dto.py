"""Class to store information about variable information about the car"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CarVariableDto:
    """ Class to represent variable attributes of cat from AUTO ESA"""
    car_variable_id: (int | None)
    car_id: (int | None)
    lowcost: bool
    premium: bool
    monthly_price: int
    special_price: int
    condition: float
    price: int
    discount: int
    datetime_captured: datetime
    job_id: (int | None)
