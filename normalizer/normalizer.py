""" Normalization Functions

This module provides a set of functions to normalize different words/values representing the same thing to a single
normalized value. Normalizers in this file also check various rules, formats and others. If the value fails one of the
rules, it should only print warning and return the value. This will allow us to react to new values, but it won't block
the insertion.
"""
import re
from enum import Enum
import datetime
import yaml
from pathlib import Path
from logs.logging_config import setup_logger

logger = setup_logger("normalizer")

brand_mapping = yaml.safe_load(Path('normalizer/brand_normalizer_mapping.yml').read_text())
gear_mapping = yaml.safe_load(Path('normalizer/gear_normalizer_mapping.yml').read_text())
fuel_mapping = yaml.safe_load(Path('normalizer/fuel_normalizer_mapping.yml').read_text())
body_mapping = yaml.safe_load(Path('normalizer/body_normalizer_mapping.yml').read_text())

class Norm(Enum):

    @staticmethod
    def normalize_url(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_url. Expected: str, Got: %s", str(type(value)))
            return value
        if not value.startswith("/"):
            logger.warning("Url does not start with '/', Got: %s", value)
            return value
        return value


    @staticmethod
    def normalize_price(value: int) -> int:
        if not isinstance(value, int):
            logger.warning("Unexpected type passed to normalize_price. Expected: int, Got: %s", str(type(value)))
            return value
        if value < 0:
            logger.warning("Price is negative, Got: %s", value)
            return value
        if value > 4000000:
            logger.warning("Price is too high, Got: %s", value)
            return value
        return value

    @staticmethod
    def normalize_image_url(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_image_url. Expected: str, Got: %s", str(type(value)))
            return value
        if not value.startswith("https://"):
            logger.warning("Image url does not start with 'https://', Got: %s", value)
            return value
        return value

    @staticmethod
    def normalize_reseller_id(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_reseller_id. Expected: str, Got: %s", str(type(value)))
            return value
        if not re.match(r"^\d+$", value):
            logger.warning("Reseller id is not a number, Got: %s", value)
            return value
        return value

    @staticmethod
    def normalize_brand(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_brand. Expected: str, Got: %s", str(type(value)))
            return value
        for brand, variations in brand_mapping.items():
            if value in variations:
                return brand
        logger.warning("Brand not found in mapping, Got: %s", value)
        return value


    @staticmethod
    def normalize_gear(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_gear. Expected: str, Got: %s", str(type(value)))
            return value
        for gear, variations in gear_mapping.items():
            if value in variations:
                return gear
        logger.warning("Gear not found in mapping, Got: %s", value)
        return value

    @staticmethod
    def normalize_full_name(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_full_name. Expected: str, Got: %s", str(type(value)))
        return value

    @staticmethod
    def normalize_engine(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_engine. Expected: str, Got: %s", str(type(value)))
        return value

    @staticmethod
    def normalize_year(value: int) -> int:
        if not isinstance(value, int):
            logger.warning("Unexpected type passed to normalize_year. Expected: int, Got: %s", str(type(value)))
            return value
        if value < 1900:
            logger.warning("Year is too low, Got: %s", value)
        if value > datetime.datetime.now().year:
            logger.warning("Year is too high, Got: %s", value)
        return value

    @staticmethod
    def normalize_power(value: int) -> int:
        if not isinstance(value, int):
            logger.warning("Unexpected type passed to normalize_power. Expected: int, Got: %s", str(type(value)))
            return value
        if value < 0:
            logger.warning("Power is negative, Got: %s", value)
        if value > 1000:
            logger.warning("Power is too high, Got: %s", value)
        return value

    @staticmethod
    def normalize_fuel(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_fuel. Expected: str, Got: %s", str(type(value)))
            return value
        for fuel, variations in fuel_mapping.items():
            if value in variations:
                return fuel
        logger.warning("Fuel not found in mapping, Got: %s", value)
        return value

    @staticmethod
    def normalize_mileage(value: int) -> int:
        if not isinstance(value, int):
            logger.warning("Unexpected type passed to normalize_mileage. Expected: int, Got: %s", str(type(value)))
            return value
        if value < 0:
            logger.warning("Mileage is negative, Got: %s", value)
        if value > 2000000:
            logger.warning("Mileage is too high, Got: %s", value)
        return value

    @staticmethod
    def normalize_equipment_class(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_equipment_class. Expected: str, Got: %s", str(type(value)))
        return value

    @staticmethod
    def normalize_body_type(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to normalize_body_type. Expected: str, Got: %s", str(type(value)))
            return value
        for body_type, variations in body_mapping.items():
            if value in variations:
                return body_type
        logger.warning("Body type not found in mapping, Got: %s", value)
        return value

    @staticmethod
    def normalize_condition(value: float) -> float:
        if not isinstance(value, float) and not isinstance(value, int):
            logger.warning("Unexpected type passed to normalize_condition. Expected: float | int, Got: %s", str(type(value)))
            return value
        if value < 0:
            logger.warning("Condition is negative, Got: %s", value)
        if value > 1:
            logger.warning("Condition is too high, Got: %s", value)
        return value

    URL = normalize_url
    IMAGE_URL = normalize_image_url
    RESELLER_ID = normalize_reseller_id
    BRAND = normalize_brand
    GEAR = normalize_gear
    FULL_NAME = normalize_full_name
    ENGINE = normalize_engine
    YEAR = normalize_year
    POWER = normalize_power
    FUEL = normalize_fuel
    MILEAGE = normalize_mileage
    EQUIPMENT_CLASS = normalize_equipment_class
    BODY_TYPE = normalize_body_type
    PRICE = normalize_price
    CONDITION = normalize_condition


def normalize_value(normalization_function: Norm):
    def inner(func):
        """ Inner function of the decorator returning the wrapper"""

        def wrapper(*args, **kwargs):
            return normalization_function.value(func(*args, **kwargs))

        return wrapper

    return inner
