# Stubs for deez.deez (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Dict, List, NoReturn, Optional, Type, Union

from deez.conf import Setting
from deez.middleware import Middleware
from deez.resource import Resource
from deez.router import Router
from deez.urls import Path


class Deez:
    router: Router = ...
    settings: Setting = ...
    middleware: List[Type[Middleware]] = ...
    middleware_reversed: List[Type[Middleware]] = ...

    def __init__(self) -> None: ...

    def _setup(self) -> NoReturn: ...

    def register_route(self, path: Union[str, Path], resource_class: Optional[Type[Resource]] = None) -> NoReturn: ...

    def process_request(self, event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]: ...