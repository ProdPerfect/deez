import asyncio
from functools import lru_cache
from typing import Any, Dict, List, Match, Tuple, Union

from deez.core.api_gateway import api_gateway_response
from deez.exceptions import (
    NoResponseError,
    NotFound,
)
from deez.logger import get_logger
from deez.middleware import Middleware
from deez.request import Request
from deez.response import BaseResponse


class Router:
    """
    The router is responsible for calling the appropriate resource classes
    and executing middleware -- it's the core of Deez.
    """

    def __init__(
        self,
        *,
        routes,
        route_patterns,
        settings,
        middleware,
        middleware_reversed,
        exception_handler,
    ) -> None:
        self._routes = routes
        self._settings = settings
        self._middleware = middleware
        self._middleware_reversed = middleware_reversed
        self._route_patterns = route_patterns
        self._exception_handler = exception_handler
        self._logger = get_logger("deez.router")

    @lru_cache(maxsize=None)
    def find_route_match(self, path: str, method: str) -> Union[None, Match]:
        """
        Find a route match for the given path and method. If no match is found,
        return None, which will raise a 404.
        """
        for pattern in self._route_patterns:
            match = pattern.match(path)
            if match and hasattr(self._routes[match.re.pattern], method):
                return match

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
        response: BaseResponse,
    ) -> BaseResponse:
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
        This is where the resource calling and middleware execution _really_ happens.
        Probably deserves a much longer comment, but I feel like for now it's pretty
        self-explanatory.
        """
        request = Request(event=event, context=context)
        path = request.path
        method = request.method.lower()

        match = self.find_route_match(path=path, method=method)
        if not match:
            raise NotFound(f"{method.upper()} '{path}' not found!")

        resource_class = self._routes[match.re.pattern]
        resource_instance = resource_class()

        # stores url arguments on the resource object, so they can
        # be used in places like middleware. e.g.: `resource.kwargs`
        kwargs = match.groupdict()
        setattr(resource_instance, "kwargs", kwargs)

        # middleware that needs to run before calling the resource
        request = self._prepare_request(self._middleware, request)

        # TODO: experimental asyncio support: should be looked at more closely?
        if asyncio.iscoroutinefunction(resource_instance.dispatch):
            response = asyncio.run(resource_instance.dispatch(request=request, **kwargs))
        else:
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
