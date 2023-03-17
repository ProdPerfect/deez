import logging
from typing import Any, Dict, List, Union, AnyStr

from deez.contrib.serialization import json_loads
from deez.helpers import method_proxy

try:
    from ujson import JSONDecodeError  # type: ignore
except ImportError:
    from json import JSONDecodeError  # type: ignore

_logger = logging.getLogger(__file__)
_methods_with_bodies = {"POST", "PATCH", "PUT"}


class Header:
    def __init__(self, data: Dict[str, str]) -> None:
        self.data = data


class Post:
    def __init__(self, body: Union[Dict, List]) -> None:
        self.data: Union[Dict, List, str, int, float, None] = None
        self.content = body
        self._loads(body)

    def _loads(self, body: Union[List, Dict, AnyStr]) -> None:
        if isinstance(body, (list, dict)):
            self.data = body
        else:
            self.data = json_loads(body)


class Get:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.params = params


class Request:
    def __init__(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
    ) -> None:
        self.path: str
        self.method: str
        self.cookies: List[str] = []
        self.aws_event = event
        self.aws_context = context
        self.version = self.aws_event.get(
            "version", "1.0"
        )  # non-http api events don't provide version information

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

        self.GET = Get(self.aws_event.get("queryStringParameters", {}))
        self.HEADERS = Header(self.aws_event.get("headers", {}))

        if self.method in _methods_with_bodies:
            self.POST = Post(self.aws_event.get("body", {}))

    def __str__(self) -> str:
        return "%s %s" % (self.method, self.path)

    def __getattr__(self, item):
        return method_proxy(self, item)
