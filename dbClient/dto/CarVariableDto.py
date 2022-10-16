from dataclasses import dataclass
from datetime import datetime
from typing import Optional

"""Class to store information about variable information about the car"""

@dataclass
class CarVariableDto:
    car_variable_id: Optional[int]
    car_id: Optional[int]
    lowcost: bool
    premium: bool
    monthly_price: int
    special_price: int
    condition: float
    price: int
    discount: int
    datetime_captured: datetime
    job_id: Optional[int]
