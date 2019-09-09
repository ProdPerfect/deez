from deez.request import Request
from deez.response import Response


class Resource:
    def get_class_name(self) -> str:
        pass

    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass

    def __call__(self, method, *args, **kwargs) -> Response:
        pass