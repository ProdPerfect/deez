import logging
from typing import Any, Dict, Optional, Union, List

from deez.contrib.serialization import json_loads
from deez.helpers import method_proxy

try:
    from ujson import JSONDecodeError  # type: ignore
except ImportError:
    from json import JSONDecodeError

_logger = logging.getLogger(__file__)


class Header:
    def __init__(self, data: Dict[str, str]) -> None:
        self.data = data

    def get(self, key: str) -> Optional[str]:
        return self.data.get(key)


class Post:
    def __init__(self, body: str) -> None:
        self.data: Dict[str, Any] = {}
        self.content = body
        self._loads(body)

    def _loads(self, body: Union[bytes, str]) -> None:
        if isinstance(body, dict):
            self.data = body

        # If we can't decode the payload automatically
        # it is up to the developer to handle dealing with
        # the content of the request.
        if isinstance(body, (str, bytes)):
            try:
                self.data = json_loads(body)
            except JSONDecodeError:
                _logger.warning(
                    "unable to decode `POST#data`. "
                    "decoding must be handled manually and is "
                    "available in POST#content."
                )

    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key)


class Get:
    def __init__(self, params: Dict[str, Any]) -> None:
        self.data = params

    def get(self, key: str) -> Optional[Any]:
        return self.data.get(key)


class Request:
    def __init__(
            self,
            event: Dict[str, Any],
            context: Dict[str, Any],
    ):
        self.path: str
        self.method: str
        self.cookies: List[str] = []
        self.aws_event = event
        self.aws_context = context
        self.version = self.aws_event['version']
        self.kwargs: Dict[str, Any] = {}

        self._build()

    def _build(self, ):
        if self.version == '1.0':
            self.path = self.aws_event['path']
            self.method = self.aws_event['httpMethod']
            self.GET = Get(self.aws_event.get('queryStringParameters', {}))
            self.POST = Post(self.aws_event.get('body', {}))
            self.HEADERS = Header(self.aws_event.get('headers', {}))
        elif self.version == '2.0':
            context = self.aws_event['requestContext']
            self.path = context['http']['path']
            self.method = context['http']['method']
            self.cookies = self.aws_event.get('cookies', [])
            self.GET = Get(self.aws_event.get('queryStringParameters', {}))
            self.POST = Post(self.aws_event.get('body', {}))
            self.HEADERS = Header(self.aws_event.get('headers', {}))

    def __str__(self):
        return '%s %s' % (self.method, self.path)

    def __getattr__(self, item):
        return method_proxy(self, item)
