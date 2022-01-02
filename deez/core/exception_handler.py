import json
import logging
from typing import Dict

from deez.core.gateway import api_gateway_response
from deez.exceptions import DeezError

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

HTTP_EXCEPTION_STATUS_CODES: Dict[str, int] = {
    "BadRequest": 400,
    "UnAuthorized": 401,
    "PermissionDenied": 403,
    "NotFound": 404,
    "MethodNotAllowed": 405,
}

HTTP_EXCEPTIONS = set(HTTP_EXCEPTION_STATUS_CODES.keys())


def handler(exc, *args, **kwargs):
    if isinstance(exc, DeezError):
        for exception in HTTP_EXCEPTIONS:
            klass_name = exc.__class__.__name__
            if exception == klass_name:
                code = HTTP_EXCEPTION_STATUS_CODES[klass_name]
                return api_gateway_response(
                    data=json.dumps({'message': exc.args[0]}),
                    status_code=code,
                )

    logger.exception("an unexpected error occurred", exc_info=True)
    return api_gateway_response(
        data=json.dumps({'message': 'internal error'}),
        status_code=500,
    )
