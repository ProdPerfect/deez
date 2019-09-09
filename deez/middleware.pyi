from deez.request import Request
from deez.response import Response
from deez.views import View


class Middleware:
    def __init__(self, view: View) -> None:
        pass

    def before_request(self, request: Request) -> Request:
        pass

    def before_response(self, response: Response) -> Response:
        pass