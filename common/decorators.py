""" Custom decorators used in this project """

from common.custom_exceptions import AttributeExtractionError


# Decorator for save extraction
def save_attribute_extraction(element):
    """ Decorator that wraps function in try catch block.
    If exception occurs during the extraction, AttributeExtractionError exception is thrown.
    The input parameter element is name of extracted element which will be used in the exception message"""

    def inner(func):
        """ Inner function of the decorator returning the wrapper"""

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                raise AttributeExtractionError(
                    f"Issue during extraction of {element} element, {exception.with_traceback(None)}, args: {args}, {kwargs}") from exception

        return wrapper

    return inner
