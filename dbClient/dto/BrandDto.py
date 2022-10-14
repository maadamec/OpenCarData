from dataclasses import dataclass

"""Class to store information about car manufactures"""


@dataclass(frozen=True)
class BrandDto:
    brand_id: int
    brand_name: str
