from dataclasses import dataclass

"""Class to store information different types of car bodies"""


@dataclass(frozen=True)
class BodyTypeDto:
    body_type_id: int
    body_type_name: str
