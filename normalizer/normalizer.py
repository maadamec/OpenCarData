""" Normalization Functions

This module provides a set of functions to normalize different words/values representing the same thing to a single
normalized value. Normalizers in this file also check various rules, formats and others. If the value fails one of the
rules, it should only print warning and return the value. This will allow us to react to new values, but it won't block
the insertion.
"""
import re
from enum import Enum

from logs.logging_config import setup_logger

logger = setup_logger("normalizer")

class Norm(Enum):

    @staticmethod
    def __normalize_url(value: str) -> str:
        if not isinstance(value, str):
            logger.warning("Unexpected type passed to __normalize_url. Expected: str, Got: %s", str(type(value)))
            return value
        if not value.startswith("/"):
            logger.warning("Url does not start with '/', Got: %s", value)
            return value
        return value


    @staticmethod
    def __normalize_price(value: int):
        return value

    @staticmethod
    def __normalize_image_url(value: str) -> str:
        return value

    @staticmethod
    def __normalize_reseller_id(value: str) -> str:
        return value

    @staticmethod
    def __normalize_brand(value: str) -> str:
        return value

    @staticmethod
    def __normalize_gear(value: str) -> str:
        return value

    @staticmethod
    def __normalize_full_name(value: str) -> str:
        return value

    @staticmethod
    def __normalize_engine(value: str) -> str:
        return value

    @staticmethod
    def __normalize_year(value: int):
        return value

    @staticmethod
    def __normalize_power(value: int):
        return value

    @staticmethod
    def __normalize_fuel(value: str) -> str:
        return value

    @staticmethod
    def __normalize_mileage(value: int):
        return value

    @staticmethod
    def __normalize_equipment_class(value: str) -> str:
        return value

    @staticmethod
    def __normalize_body_type(value: str) -> str:
        return value

    @staticmethod
    def __normalize_condition(value: float) -> float:
        return value

    URL = __normalize_url
    IMAGE_URL = __normalize_image_url
    RESELLER_ID = __normalize_reseller_id
    BRAND = __normalize_brand
    GEAR = __normalize_gear
    FULL_NAME = __normalize_full_name
    ENGINE = __normalize_engine
    year = __normalize_year
    POWER = __normalize_power
    FUEL = __normalize_fuel
    MILEAGE = __normalize_mileage
    EQUIPMENT_CLASS = __normalize_equipment_class
    BODY_TYPE = __normalize_body_type
    PRICE = __normalize_price
    CONDITION = __normalize_condition


def normalize_value(normalization_function: Norm):
    def inner(func):
        """ Inner function of the decorator returning the wrapper"""

        def wrapper(*args, **kwargs):
            return normalization_function.value(func(*args, **kwargs))

        return wrapper

    return inner
