import logging
from typing import Any, Dict

from deez.contrib.serialization import json_dumps
from deez.core.gateway import api_gateway_response
from deez.exceptions import DeezError

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

CLIENT_EXCEPTION_STATUS_CODES: Dict[str, int] = {
    "BadRequest": 400,
    "UnAuthorized": 401,
    "Forbidden": 403,
    "NotFound": 404,
    "MethodNotAllowed": 405,
    "UnsupportedMediaType": 415,
    "TooManyRequests": 429,
}

CLIENT_EXCEPTION_NAMES = set(CLIENT_EXCEPTION_STATUS_CODES.keys())


def handler(exc: Exception) -> Dict[str, Any]:
    """generic exception handler"""
    exc_class = exc.__class__.__name__
    if isinstance(exc, DeezError) and exc_class in CLIENT_EXCEPTION_NAMES:
        code = CLIENT_EXCEPTION_STATUS_CODES[exc_class]
        return api_gateway_response(
            data=json_dumps({"message": exc.args[0]}),
            status_code=code,
        )

    logger.exception("an unexpected error occurred", exc_info=True)
    return api_gateway_response(
        data=json_dumps({"message": "internal error"}),
        status_code=500,
    )
