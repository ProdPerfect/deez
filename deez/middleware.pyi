from deez.request import Request
from deez.response import Response
from deez.resource import Resource


class Middleware:
    def __init__(self, view: Resource) -> None:
        pass

    def before_request(self, request: Request) -> Request:
        pass

    def before_response(self, response: Response) -> Response:
        pass