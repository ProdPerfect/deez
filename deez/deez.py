from typing import Iterable, List

from deez.conf import settings
from deez.middleware import Middleware
from deez.router import Router
from deez.utils import resolve_middleware_classes


class Deez:
    def __init__(self) -> None:
        self.router: Router = None
        self.settings = settings
        self.middleware: List[Middleware] = []
        self.middleware_reversed: Iterable[Middleware] = []

        self._setup()

    def _setup(self) -> None:
        self.route = Router(self)
        if hasattr(self.settings, 'MIDDLEWARE'):
            self.middleware = resolve_middleware_classes(self.settings.MIDDLEWARE)
            self.middleware_reversed = reversed(self.middleware)

    def register_route(self, path: str, resource_class) -> None:
        self.router.register(path=path, resource=resource_class)

    def process_request(self, event, context):
        assert self.router is not None
        return self.router.route(event, context)
