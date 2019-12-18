from typing import Any, Dict

try:
    import ujson as json
except ImportError:
    import json


class Response:

    def __init__(self, data: Any = None, status_code: int = 200, headers: Dict[str, str] = None) -> None:
        self.data = data
        self.headers = headers
        self.status_code = status_code

    def render(self, *args, **kwargs) -> Any:
        return self.data


class JsonResponse(Response):

    def render(self, *args, **kwargs) -> str:
        return json.dumps(self.data)
