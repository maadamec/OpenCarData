from common.CustomException import AttributeExtractionError


# Decorator for save extraction
def save_attribute_extraction(element):
    def inner(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise AttributeExtractionError(
                    f"Issue during extraction of {element} element, {e.with_traceback(None)}")
        return wrapper

    return inner