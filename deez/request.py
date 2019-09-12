import re
from functools import lru_cache
from typing import Iterable

CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


# https://stackoverflow.com/a/29916095
# TODO: Think of a better way to do this, it's kind of slow.
@lru_cache(maxsize=100)
def _camel_case_split(identifier):
    matches = CAMELCASE_REGEX.finditer(identifier)
    split_string = []
    previous = 0
    for match in matches:
        split_string.append(identifier[previous:match.start()])
        previous = match.start()
    split_string.append(identifier[previous:])
    return split_string


class Request:
    def __init__(self, event, context):
        self.lambda_context = context
        self._cleaned_event = {}
        self._parse_event(event)

    @staticmethod
    def _fixup_keys(key):
        """
        Turns camel-case into snake-case
        For example: queryStringParameters -> query_string_parameters

        Note: This only done for the top-level keys.
        """
        return '_'.join(_camel_case_split(key)).lower()

    def _parse_event(self, event: dict):
        for k, v in event.items():
            key = self._fixup_keys(k)
            self._cleaned_event[key] = v
            setattr(self, key, v)
        return self

    def __dir__(self) -> Iterable[str]:
        return [k for k in self._cleaned_event.keys()]

    def __str__(self):
        return f'Request: {self._cleaned_event}'

    def __getattr__(self, item):
        return getattr(self, item)