from abc import abstractmethod
from typing import Any, Dict, Optional, Union

from deez.contrib.serialization import json_dumps


class Response:
    def __init__(
        self,
        data: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, Any]] = None,
        content_type: Union[str, None] = None,
    ) -> None:
        self.data = data
        self.headers = {}
        if headers:
            self.headers = headers
        self.status_code = status_code
        self.content_type = content_type

    @abstractmethod
    def render(self, *args, **kwargs) -> str:
        pass


class NoContentResponse(Response):
    def __init__(self, headers: Union[Dict[str, Any], None] = None) -> None:
        super().__init__(headers=headers, status_code=204)

    def render(self, *args, **kwargs) -> Optional[str]:
        return None


class JsonResponse(Response):
    def __init__(
        self,
        data=None,
        status_code: int = 200,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            data=data,
            status_code=status_code,
            headers=headers,
            content_type="application/json",
        )

    def render(self, *args, **kwargs) -> str:
        return json_dumps(self.data)


class HttpRedirectResponse(Response):
    def __init__(
        self,
        location: str,
        status_code: int = 302,
        headers: Union[Dict[str, Any], None] = None,
    ) -> None:
        location_header = {"Location": location}
        if headers:
            headers.update(location_header)
        else:
            headers = location_header
        super().__init__(
            status_code=status_code,
            headers=headers,
            content_type="application/json",
        )

    def render(self, *args, **kwargs) -> Optional[str]:
        return None
