import json
import re
from functools import lru_cache
from typing import Any, Dict, List, Optional

CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


# https://stackoverflow.com/a/29916095
# TODO: Think of a better way to do this, it's kind of slow.
def _camel_case_split(identifier: str) -> List[str]:
    matches = CAMELCASE_REGEX.finditer(identifier)
    split_string = []
    previous = 0
    for match in matches:
        split_string.append(identifier[previous:match.start()])
        previous = match.start()
    split_string.append(identifier[previous:])
    return split_string


class Header:
    def __init__(self, headers: Dict[str, str]) -> None:
        self._headers = headers

    def __getattr__(self, item: str) -> Optional[str]:
        return self._headers.get(item.lower())


class Post:
    def __init__(self, body: str) -> None:
        self.data = self._loads(body)

    @staticmethod
    def _loads(body: str) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if isinstance(body, str):
            data = json.loads(body)
        return data

    def get(self, key: str) -> Optional[str]:
        return self.data.get(key)


class Get:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.data = params

    def get(self, key: str) -> Optional[str]:
        return self.data.get(key)


class Request:
    def __init__(self, event, context):
        self.lambda_context = context
        self._raw_event = event
        self._cleaned_event = {}
        self._parse_event(event)

        self.GET = Get(event.get('queryStringParameters', {}))
        self.POST = Post(event.get('body', {}))
        self.HEADERS = Header(event.get('headers', {}))

    @property
    def method(self) -> str:
        return self._cleaned_event.get('http_method')

    @staticmethod
    @lru_cache(maxsize=10000)
    def _fixup_keys(key: str) -> str:
        """
        Turns camel-case into snake-case
        For example: queryStringParameters -> query_string_parameters

        Note: This only done for the top-level keys.
        """
        return '_'.join(_camel_case_split(key)).lower()

    def _parse_event(self, event):
        for k, v in event.items():
            key = self._fixup_keys(k)
            self._cleaned_event[key] = v
        return self

    def __dir__(self):
        return self._cleaned_event.keys()

    def __str__(self):
        return f'Request: {self._cleaned_event}'

    def __getattr__(self, item: str) -> Any:
        return self._cleaned_event[item]
