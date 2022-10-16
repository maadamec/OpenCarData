from dataclasses import dataclass
from datetime import datetime
from typing import Optional

"""Class to store information from the EsaCar website"""

@dataclass
class CarDto:
    car_id: Optional[int]
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
    job_id: Optional[int]
