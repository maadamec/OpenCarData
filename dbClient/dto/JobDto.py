from dataclasses import dataclass
from datetime import datetime
from typing import Optional

"""Class to store information about job"""

@dataclass
class JobDto:
    job_id: Optional[int]
    job_name: str
    datetime_start: datetime
    datetime_end: datetime
    detail: str
