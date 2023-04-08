"""Class to store information about job"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class JobDto:
    """ Class to represent job run """
    job_id: (int | None)
    job_name: str
    datetime_start: datetime
    datetime_end: (datetime | None)
    detail: str
