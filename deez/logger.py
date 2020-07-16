import logging
from functools import lru_cache


@lru_cache()
def get_logger():
    from deez.conf import settings
    fmt = '%(asctime)s %(levelname)s %(message)s'
    logging.basicConfig(format=fmt)
    logger = logging.getLogger('deez')
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
