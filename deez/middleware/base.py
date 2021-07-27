from typing import Pattern, Optional

from deez.request import Request
from deez.response import Response


class Middleware:
    """
    base class for implementing middleware
    """

    def __init__(self) -> None:
        self.path_regex: Optional[Pattern] = None

    def before_request(self, request: Request) -> Request:
        return request

    def before_response(self, response: Response) -> Response:
        return response

    def run(self, path: str) -> bool:
        return bool(self.path_regex and self.path_regex.match(path))
