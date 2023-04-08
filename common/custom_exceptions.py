""" Module for custom exceptions """


class CarSoldOutException(Exception):
    """ Exception thrown when the car is sold out,
    and we don't need to extract data from the page """


class AttributeExtractionError(Exception):
    """ Exception thrown when an attribute couldn't be extracted due to some issue """
