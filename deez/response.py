import json
from typing import Any, Dict


class Response:

    def __init__(self, data: Any = None,
                 status_code: int = 200,
                 headers: Dict[str, str] = None,
                 content_type: str = None) -> None:
        self.data = data
        self.headers = headers
        self.status_code = status_code
        self.content_type = content_type

    def render(self, *args, **kwargs) -> Any:
        return self.data


class NoContentResponse(Response):
    def __init__(self, headers: Dict[str, str] = None):
        super().__init__(headers=headers, status_code=204)

    def render(self, *args, **kwargs) -> Any:
        return None


class JsonResponse(Response):
    def __init__(self, data: Any = None, status_code: int = 200, headers: Dict[str, str] = None):
        super().__init__(data=data, status_code=status_code, headers=headers, content_type='application/json')

    def render(self, *args, **kwargs) -> str:
        return json.dumps(self.data)
