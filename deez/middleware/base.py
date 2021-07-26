from re import Pattern
from typing import Optional

from deez.request import Request
from deez.response import Response


class Middleware:
    """
    base class for implementing middleware
    """

    def __init__(self) -> None:
        self.path_regex: Optional[Pattern] = None

    @property
    def is_scoped(self) -> bool:
        return True if self.path_regex else False

    def before_request(self, request: Request) -> Request:
        return request

    def before_response(self, response: Response) -> Response:
        return response

    def run(self, path: str) -> bool:
        return (not self.is_scoped
                or (self.is_scoped and self.path_regex.match(path)))
