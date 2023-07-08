from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Job:
    """ Class to represent job run """
    job_id: int
    job_name: str
    datetime_start: datetime
    datetime_end: (datetime | None)
    detail: str
