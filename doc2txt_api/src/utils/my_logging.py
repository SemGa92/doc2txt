import os
import logging
from functools import wraps


MY_DEBUG = os.getenv("MY_DEBUG", 'False').lower() in ('true', '1')


if MY_DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s | %(asctime)s | %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

LOGGER = logging.getLogger(__name__)

logging.getLogger("pdfminer").setLevel(logging.WARNING)


def debug(f):
    """Decorator for adding debug logs to a function"""
    @wraps(f)
    def inner(*args, **kwargs):
        """
        #f"Calling {f.__name__} with args: {args}, kwargs: {kwargs}"
        #f"{f.__name__} returned: {result}"
        """
        LOGGER.debug(f"Start {f.__name__}")
        result = f(*args, **kwargs)
        LOGGER.debug(f"End   {f.__name__}")
        return result
    return inner
