import logging
from functools import lru_cache


@lru_cache()
def get_logger():
    from deez.conf import settings
    logging.basicConfig(format=settings.LOGGER_MESSAGE_FORMAT)
    logger = logging.getLogger('deez')
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
