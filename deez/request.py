import json
import re
from functools import lru_cache

CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')


# https://stackoverflow.com/a/29916095
# TODO: Think of a better way to do this, it's kind of slow.
def _camel_case_split(identifier):
    matches = CAMELCASE_REGEX.finditer(identifier)
    split_string = []
    previous = 0
    for match in matches:
        split_string.append(identifier[previous:match.start()])
        previous = match.start()
    split_string.append(identifier[previous:])
    return split_string


class Post:
    def __init__(self, body):
        self._data = None
        self._setup(body)

    def _setup(self, body):
        if isinstance(body, str):
            self._data = json.loads(body)

    def get(self, key):
        return self._data.get(key)


class Get:
    def __init__(self, params):
        self._data = None
        self._setup(params)

    def _setup(self, params):
        self._data = params

    def get(self, key):
        return self._data.get(key)


class Request:
    def __init__(self, event, context):
        self.lambda_context = context
        self._cleaned_event = {}
        self._parse_event(event)

        self.GET = Get(event.get('queryStringParameters', {}))
        self.POST = Post(event.get('body'))

    @staticmethod
    @lru_cache(maxsize=100)
    def _fixup_keys(key):
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

    def __getattr__(self, item):
        return self._cleaned_event[item]
