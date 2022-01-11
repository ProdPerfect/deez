import logging
import re
from typing import Type, Union, List, Dict, Pattern, Any

from deez.conf import Setting
from deez.core.router import Router
from deez.core.signals import (
    application_setup_finished,
    application_setup_started,
    application_routes_registered,
)
from deez.exceptions import DuplicateRouteError
from deez.middleware import Middleware
from deez.resource import Resource
from deez.urls import Path
from deez.utils import import_resolver, middleware_resolver

logging.basicConfig(
    format="%(name)s: %(asctime)s %(levelname)s %(message)s"
)

_logger = logging.getLogger('deez')


class Deez:
    def __init__(self) -> None:
        self.router: Router
        self.routes: Dict[str, Type[Resource]] = {}
        self.settings: Setting
        self.middleware: List[Middleware] = []
        self.route_patterns: List[Pattern] = []
        self.middleware_reversed: List[Middleware] = []
        self._setup()

    def _setup(self) -> None:
        # notify subscribers that setup has started
        application_setup_started.send(self)

        from deez.conf import settings

        self.settings = settings
        if hasattr(settings, 'MIDDLEWARE'):
            self.middleware = middleware_resolver(settings.MIDDLEWARE)
            self.middleware_reversed = list(reversed(self.middleware))

        self.router = Router(
            routes=self.routes,
            settings=settings,
            middleware=self.middleware,
            route_patterns=self.route_patterns,
            middleware_reversed=self.middleware_reversed,
            exception_handler=import_resolver(settings.EXCEPTION_HANDLER)
        )

        # notify subscribers that setup has finished
        application_setup_finished.send(self)

    def register_route(self, path, resource_class=None) -> None:
        self._register(path=path, resource=resource_class)

    def register_routes(self, paths: List[Path]) -> None:
        """register routes in bulk"""
        assert isinstance(paths, (list, tuple))
        assert len(paths) > 0, "expected at least one path"
        for path in paths:
            self.register_route(path)

        application_routes_registered.send(self, routes=self.routes)

    def _validate_path(self, path):
        if path in self.routes:
            raise DuplicateRouteError(f"\"{path}\" already defined")

    def _register(self, path, resource=None):
        """
        Add a path to its internal registry with some validation
        to prevent duplicate routes from being registered.
        """
        raw_url: str = path
        url_path: Union[str, Path] = path
        url_resource: Type[Resource] = resource

        if isinstance(path, Path):
            raw_url = path.raw_url
            url_path = path.regex
            url_resource = path.resource

        assert url_resource is not None
        assert issubclass(url_resource, Resource), \
            "resource must be a subclass of deez.resource.Resource"

        self._validate_path(url_path)

        _logger.debug("registering URL path '%s'", raw_url)

        self.routes[url_path] = url_resource
        self.route_patterns.append(re.compile(str(url_path)))

    def process_request(self, event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        return self.router.route(event, context)
