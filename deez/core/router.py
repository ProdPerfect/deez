import re
from functools import lru_cache
from typing import Any, Dict, List, Match, Optional, Tuple, Union

from deez.core.gateway import api_gateway_response
from deez.exceptions import (
    NoResponseError,
    NotFound,
)
from deez.logger import get_logger
from deez.middleware import Middleware
from deez.request import Request
from deez.response import Response


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
    def _get_re_match(self, path: str, method: str) -> Union[None, Match]:
        self._logger.debug("finding URL pattern match for path: '%s'", path)
        matched_patterns = [pattern.search(path) for pattern in self._route_patterns]

        matched_patterns = list(filter(None, matched_patterns))
        if not matched_patterns:
            self._logger.debug("no matching URL patterns found for path: '%s'", path)
            return None

        matched_patterns_length = len(matched_patterns)

        self._logger.debug(
            "%s matching URL patterns found for path: '%s'",
            matched_patterns_length,
            path,
        )

        if matched_patterns_length > 1:
            best_match = [
                match
                for match in matched_patterns
                if match and hasattr(self._routes[match.re.pattern], method)
            ]

            best_match_count = len(best_match)

            # method required to serve this request was not implemented
            if best_match_count == 0:
                return None

            if best_match_count == 1:
                return best_match[0]

            best_pattern: re.Match = best_match[0]  # default best match
            best_group_count = 0

            for best in best_match:
                re_pattern = best.re.pattern
                exact_pattern = self._routes.get(re_pattern)
                if exact_pattern:
                    best_pattern = best
                    break

                groups_len = len(best.groups())
                if groups_len > best_group_count:
                    best_pattern = best
                    best_group_count = groups_len

            self._logger.debug(
                "URL pattern '%s' was best match for path: '%s'",
                best_pattern.re.pattern,
                path,
            )
            return best_pattern

        return matched_patterns[0]

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
        response: Response,
    ) -> Response:
        for mw in middleware:
            if hasattr(mw, "before_response") and mw.run(request.path):
                mw.before_response(response=response)
        return response

    def execute(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Tuple[Optional[str], int, Dict[str, Any], str]:
        """
        This is where the resource calling and middleware execution _really_ happens.
        Probably deserves a much longer comment, but I feel like for now it's pretty
        self-explanatory.
        """
        request = Request(event=event, context=context)
        path = request.path
        method = request.method.lower()

        re_match = self._get_re_match(path=path, method=method)
        if not re_match:
            raise NotFound(f"{method.upper()} '{path}' not found!")

        resource_class = self._routes[re_match.re.pattern]
        resource_instance = resource_class()

        # stores url arguments on the request object so they can
        # be used in places like middleware.
        kwargs = re_match.groupdict()
        setattr(
            request, "kwargs", kwargs
        )  # TODO: deprecate and use `resource.kwargs` instead
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
            response, status_code, headers, content_type = self.execute(
                event=event, context=context
            )
            return api_gateway_response(
                status_code=status_code,
                data=response,
                content_type=content_type,
                extra_headers=headers,
            )
        except RuntimeError as exc:
            return self._exception_handler(exc)
