# Stubs for deez.request (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Dict, Optional


class Header:
    _headers: Dict[str, str] = ...

    def __init__(self, headers: Dict[str, str]) -> None: ...

    def get(self, key: str) -> Optional[str]: ...


class Post:
    data: Dict[str, Any] = ...

    def __init__(self, body: str) -> None: ...

    def get(self, key: str) -> Optional[Any]: ...

    def _loads(self, data: str) -> Dict[str, Any]: ...


class Get:
    data: Dict[str, Any] = ...

    def __init__(self, params: Dict[str, Any]) -> None: ...

    def get(self, key: str) -> Optional[Any]: ...


class Request:
    lambda_context: Dict[str, Any] = ...
    raw_event: Dict[str, Any] = ...
    GET: Get = ...
    POST: Post = ...
    METHOD: str = ...
    HEADERS: Header = ...

    def __init__(self, event: Dict[str, Any], context: Dict[str, Any]) -> None: ...

    @property
    def method(self) -> str: ...

    @property
    def path(self) -> str: ...
