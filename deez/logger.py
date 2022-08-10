import logging

from deez.conf import settings

logging.basicConfig(
    format="%(name)s: %(asctime)s %(levelname)s %(message)s"
)


def get_logger(name: str = 'deez') -> logging.Logger:
    logger = logging.getLogger(name)
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger
