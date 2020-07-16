import json
from abc import abstractmethod
from typing import Optional


class Response:

    def __init__(self, data=None, status_code=200, headers=None, content_type=None):
        self.data = data
        self.headers = headers
        self.status_code = status_code
        self.content_type = content_type

    @abstractmethod
    def render(self, *args, **kwargs) -> Optional[str]:
        pass


class NoContentResponse(Response):
    def __init__(self, headers=None):
        super().__init__(headers=headers, status_code=204)

    def render(self, *args, **kwargs) -> Optional[str]:
        return None


class JsonResponse(Response):
    def __init__(self, data=None, status_code=200, headers=None):
        super().__init__(data=data, status_code=status_code, headers=headers, content_type='application/json')

    def render(self, *args, **kwargs) -> Optional[str]:
        return json.dumps(self.data)
