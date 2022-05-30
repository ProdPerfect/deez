from typing import Pattern, Optional

from deez import Request, Response


class Middleware:
    """
    base class for implementing middleware
    """

    def __init__(self, path_regex: Optional[Pattern] = None) -> None: ...
    def run(self, path: str) -> bool: ...
    def before_request(self, request: Request) -> Request: ...
    def before_response(self, response: Response) -> Response: ...
