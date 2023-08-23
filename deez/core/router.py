from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Callable, Dict, List, Match, Tuple, Type, Union, Pattern

from deez.core.api_gateway import api_gateway_response
from deez.exceptions import NoResponseError, NotFound
from deez.logger import get_logger
from deez.middleware import Middleware
from deez.request import Request
from deez.resource import Resource
from deez.response import JsonResponse
import typing

if typing.TYPE_CHECKING:
    from deez.conf import Setting


@dataclass
class RouteMatch:
    """
    A route match is a tuple of a compiled regex pattern and the resource class
    that should be called when a match is found.
    """

    re_match: Match
    resource: Type[Resource]

    def __bool__(self) -> bool:
        return all([self.re_match, self.resource])


class Router:
    """
    The router is responsible for calling the appropriate resource classes
    and executing middleware -- it's the core of Deez.
    """

    def __init__(
        self,
        *,
        routes: Dict[str, Type[Resource]],
        route_patterns: List[Pattern[str]],
        settings: "Setting",
        middleware: List[Middleware],
        middleware_reversed: List[Middleware],
        exception_handler: Callable[..., Dict[str, Any]],
    ) -> None:
        self._routes = routes
        self._settings = settings
        self._middleware = middleware
        self._middleware_reversed = middleware_reversed
        self._route_patterns = route_patterns
        self._exception_handler = exception_handler
        self._logger = get_logger("deez.router")

    @lru_cache(maxsize=None)
    def find_route_match(self, path: str, method: str) -> Union[RouteMatch, None]:
        """
        Find a route match for the given path and method. If no match is found,
        return None, which will raise a 404.
        """

        for pattern in self._route_patterns:
            match = pattern.match(path)
            if match and match.re.pattern in self._routes:
                resource = self._routes[match.re.pattern]
                # check if the resource has the method we're looking for
                if hasattr(resource, method):
                    return RouteMatch(re_match=match, resource=resource)

        return None

    def _prepare_request(
        self,
        middleware: List[Middleware],
        request: Request,
    ) -> Request:
        for mw in middleware:
            if hasattr(mw, "before_request") and mw.run(request.path):
                mw.before_request(request=request)
        return request

    def _prepare_response(
        self,
        middleware: List[Middleware],
        request: Request,
        response: JsonResponse,
    ) -> JsonResponse:
        for mw in middleware:
            if hasattr(mw, "before_response") and mw.run(request.path):
                mw.before_response(response=response)
        return response

    def execute(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[Union[bytes, None], int, Dict[str, Any], str]:
        """
        Entry point into the router.

        At a high level, the router does the following:
        1. Find a route match
        2. Instantiate the resource class
        3. Call the resource class
        4. Return the response
        """

        request = Request(event=event, context=context)
        path = request.path
        method = request.method.lower()

        match = self.find_route_match(path=path, method=method)
        if not match:
            raise NotFound(f"{method.upper()} '{path}' not found!")

        # instantiate the resource class
        resource_instance = match.resource()

        # stores url arguments on the resource object, so they can
        # be used in places like middleware. e.g.: `resource.kwargs`
        kwargs = match.re_match.groupdict()
        setattr(resource_instance, "kwargs", kwargs)

        # middleware that needs to run before calling the resource
        request = self._prepare_request(self._middleware, request)

        response = resource_instance.dispatch(request=request, **kwargs)
        if not response:
            raise NoResponseError(f"{resource_instance} did not return a response")

        # middleware that needs to run before response
        response = self._prepare_response(self._middleware_reversed, request, response)

        return (
            response.render(),
            response.status_code,
            response.headers,
            response.content_type,
        )

    def route(self, event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """entry point into router"""
        try:
            response, status_code, headers, content_type = self.execute(event=event, context=context)
            return api_gateway_response(
                status_code=status_code,
                data=response,
                content_type=content_type,
                extra_headers=headers,
            )
        except RuntimeError as exc:
            return self._exception_handler(exc)
