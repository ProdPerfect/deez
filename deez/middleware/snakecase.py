from functools import lru_cache
from typing import List

from deez.conf import settings
from deez.middleware.base import Middleware


# https://stackoverflow.com/a/29916095
def _camel_case_split(identifier: str) -> List[str]:
    matches = settings.CAMELCASE_REGEX.finditer(identifier)
    split_string = []
    previous = 0
    for match in matches:
        split_string.append(identifier[previous:match.start()])
        previous = match.start()
    split_string.append(identifier[previous:])
    return split_string


@lru_cache(maxsize=None)
def _fixup_keys(key: str) -> str:
    """
    Turns camel-case into snake-case
    For example: queryStringParameters -> query_string_parameters
    """
    return '_'.join(_camel_case_split(key)).lower()


def _recursively_fixup(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = _recursively_fixup(v)
        new[_fixup_keys(k)] = v
    return new


class SnakeCaseMiddleware(Middleware):
    """
    convert camelcase keys to snake case
    """

    def before_request(self, request):
        if request.GET.data:
            data = request.GET.data
            request.GET.data = _recursively_fixup(data)

        if request.POST.data:
            data = request.POST.data
            request.POST.data = _recursively_fixup(data)
        return request
