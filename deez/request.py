import sys
from typing import Any, Dict, List, Union

from deez.contrib.serialization import json_loads, json
from deez.helpers import method_proxy


class _DictMixin:
    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return "<%s>" % self.__class__.__name__

    def __iter__(self) -> Any:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, _DictMixin):
            return self._data == __value._data
        return self._data == __value

    def __getitem__(self, key: str) -> Union[Any, None]:
        return self._data.get(key)

    def as_dict(self) -> Dict[str, Any]:
        return self._data


class HeaderDict(_DictMixin):
    """
    A simple wrapper that behaves somewhat like a dictionary
    and provides a consistent interface for accessing request headers.

    Header names are case-insensitive.

    Example:
        >>> headers = HeaderDict({"Content-Type": "application/json"})
        >>> headers["content-type"]
        "application/json"
    """

    def __init__(self, data: Dict[str, str]) -> None:
        super().__init__(data)
        self._lowercase_keys(self._data)

    def _lowercase_keys(self, data) -> None:
        """
        Lowercase all keys so that headers are case-insensitive.
        """
        self._data = {k.lower(): v for k, v in data.items()}


class BodyDict(_DictMixin):
    """
    A simple wrapper that behaves somewhat like a dictionary
    and provides a consistent interface for accessing the request body.
    """

    def __init__(self, data: Any) -> None:
        super().__init__(data)
        self._loads(data)
        self.size = sys.getsizeof(data)
        self.content = data

    def _loads(self, data: Union[str, bytes, bytearray]) -> None:
        try:
            self._data = json_loads(data)
        except (json.JSONDecodeError, TypeError):
            # TODO: warn about invalid JSON
            self._data = {}


class QueryDict(_DictMixin):
    """
    A simple wrapper that behaves somewhat like a dictionary
    and provides a consistent interface for accessing the query parameters.
    """

    pass


class Request:
    def __init__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
    ) -> None:
        self.path: str
        self.data: BodyDict
        self.params: QueryDict
        self.headers: HeaderDict
        self.method: str
        self.cookies: List[str] = []
        self.aws_event = event
        self.aws_context = context
        self.version = self.aws_event.get("version", "1.0")

        self._build()

    def _build(self) -> None:
        if self.version == "1.0":
            self.path = self.aws_event["path"]
            self.method = self.aws_event["httpMethod"]
        elif self.version == "2.0":
            context = self.aws_event["requestContext"]
            self.path = context["http"]["path"]
            self.method = context["http"]["method"]
            self.cookies = self.aws_event.get("cookies", [])

        self.data = BodyDict(self.aws_event.get("body", {}))
        self.params = QueryDict(self.aws_event.get("queryStringParameters", {}))
        self.headers = HeaderDict(self.aws_event.get("headers", {}))

    def __str__(self) -> str:
        return "%s %s" % (self.method, self.path)

    def __getattr__(self, item) -> Any:
        return method_proxy(self, item)
