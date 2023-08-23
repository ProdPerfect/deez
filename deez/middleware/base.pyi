from typing import Pattern, Union

from deez import Request, BaseResponse

class Middleware:
    """
    base class for implementing middleware
    """

    path_regex: Union[Pattern, None]

    def __init__(self, path_regex: Union[Pattern, None] = None) -> None: ...
    def run(self, path: str) -> bool: ...
    def before_request(self, request: Request) -> Request: ...
    def before_response(self, response: BaseResponse) -> BaseResponse: ...
