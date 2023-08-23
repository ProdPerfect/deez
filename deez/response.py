from abc import abstractmethod
from typing import Any, Dict, Union

from deez.contrib.serialization import json_dumps


class BaseResponse:
    def __init__(
        self,
        data: Any = None,
        status_code: int = 200,
        headers: Union[Dict[str, Any], None] = None,
        content_type: str = "application/json",
    ) -> None:
        self.data = data
        self.headers = {}
        if headers:
            self.headers = headers
        self.status_code = status_code
        self.content_type = content_type

    @abstractmethod
    def render(self, *args, **kwargs) -> Union[bytes, None]:
        pass


class NoContentResponse(BaseResponse):
    def __init__(self, headers: Union[Dict[str, Any], None] = None) -> None:
        super().__init__(headers=headers, status_code=204)

    def render(self, *args, **kwargs) -> None:
        return None


class JsonResponse(BaseResponse):
    def __init__(
        self,
        data: Union[Dict[str, Any], None] = None,
        status_code: int = 200,
        headers: Union[Dict[str, Any], None] = None,
    ) -> None:
        super().__init__(
            data=data,
            status_code=status_code,
            headers=headers,
        )

    def render(self, *args, **kwargs) -> bytes:
        return json_dumps(self.data)
