import json
import re
from functools import lru_cache
from typing import Any, Dict, Optional, Tuple, Type, Union

from deez.exceptions import BadRequest, DuplicateRouteError, NoResponseError, NotFound, PermissionDenied, UnAuthorized
from deez.logger import get_logger
from deez.request import Request
from deez.resource import Resource
from deez.response import Response
from deez.urls import Path


class Router:
    """
    The router is responsible for calling the appropriate resource classes
    and executing middleware -- it's the core of Deez.
    """

    def __init__(self, app):
        self._app = app
        self._routes = {}
        self._route_names = {}
        self._route_patterns = []
        self._logger = get_logger()

    @lru_cache(maxsize=1000)
    def _get_re_match(self, path: str, method: str):
        self._logger.debug("finding URL pattern match for path: '%s'", path)
        matched_patterns = [
            pattern.search(path)
            for _, pattern in enumerate(self._route_patterns)
        ]

        if not matched_patterns:
            self._logger.debug("no matching URL patterns found for path: '%s'", path)
            return None

        if len(matched_patterns) > 1:
            self._logger.debug("at least one matching URL pattern found for path: '%s'", path)
            best_match = [
                match for _, match in enumerate(matched_patterns)
                if match and hasattr(self._routes[match.re.pattern], method)
            ]

            best_match_count = len(best_match)

            # method required to serve this request was not implemented
            if best_match_count == 0:
                return None

            if best_match_count == 1:
                return best_match[0]

            best_pattern = None
            best_group_count = 0

            for _, best in enumerate(best_match):
                re_pattern = best.re.pattern
                exact_pattern = self._routes.get(re_pattern)
                if exact_pattern:
                    best_pattern = best
                    break

                groups_len = len(best.groups())
                if groups_len > best_group_count:
                    best_pattern = best
                    best_group_count = groups_len

            self._logger.debug("URL pattern '%s' was best match for path: '%s'",
                               best_pattern.re.pattern, path)
            return best_pattern

        return matched_patterns[0]

    def execute(self, event: Dict[str, Any] = None,
                context: Dict[str, Any] = None) -> Tuple[Optional[str], int, Dict[str, Any], str]:
        """
        This is where the resource calling and middleware execution _really_ happens.
        Probably deserves a much longer comment, but I feel like for now it's pretty
        self explanatory.
        """
        request = Request(event, context=context)
        path = request.path
        method = request.method.lower()

        re_match = self._get_re_match(path=path, method=method)
        if not re_match:
            raise NotFound(f'{method.upper()} \'{path}\' not found!')

        resource_class = self._routes[re_match.re.pattern]()

        # middleware that needs to run before calling the resource
        middleware_forward = self._app.middleware
        middleware_reversed = self._app.middleware_reversed

        for _, middleware in enumerate(middleware_forward):
            _request = middleware(resource=resource_class).before_request(request=request)
            if not _request:
                raise RuntimeError(f"{middleware.__name__}.before_request did not return request object")
            request = _request

        kwargs = re_match.groupdict()
        response: Response = resource_class.dispatch(method=method, request=request, **kwargs)
        if not response:
            raise NoResponseError(f'{resource_class.get_class_name()} did not return a response')

        # middleware that needs to run before response
        for _, middleware in enumerate(middleware_reversed):
            _response = middleware(resource=resource_class).before_response(response=response)
            if not _response:
                raise RuntimeError(f"{middleware.__name__}.before_response did not return response object")
            response = _response

        return (
            response.render(),
            response.status_code,
            response.headers,
            response.content_type,
        )

    def _validate_path(self, path):
        if path in self._routes:
            raise DuplicateRouteError(f"\"{path}\" already defined")

    def register(self, path, resource=None):
        """
        Add a path to its internal registry with some validation
        to prevent duplicate routes from being registered.
        """
        url_path: Union[str, Path] = path
        url_resource: Type[Resource] = resource

        if isinstance(path, Path):
            url_path = path.regex
            url_resource = path.resource

        assert url_resource is not None
        assert issubclass(url_resource, Resource), \
            "resource must be a subclass of deez.resource.Resource"

        self._logger.debug("registering URL pattern '%s'", url_path)

        self._validate_path(url_path)
        self._routes[url_path] = url_resource
        self._route_patterns.append(re.compile(str(url_path)))

    def route(self, event, context):
        """
        Handles Deez exceptions thrown in middleware and resources
        and maps them to valid responses and status codes.
        """
        try:
            response, status_code, headers, content_type = self.execute(event=event, context=context)
            return self._make_response(status_code, response,
                                       content_type=content_type, extra_headers=headers)
        except BadRequest as exc:
            return self._make_response(400, data=json.dumps({'message': exc.args[0]}))
        except UnAuthorized as exc:
            return self._make_response(401, data=json.dumps({'message': exc.args[0]}))
        except PermissionDenied as exc:
            return self._make_response(403, data=json.dumps({'message': exc.args[0]}))
        except NotFound as exc:
            return self._make_response(404, data=json.dumps({'message': exc.args[0]}))

    def _make_response(self, status_code, data, content_type='application/json', extra_headers=None):
        default_headers = {
            'Access-Control-Allow-Origin': '*',
            'X-Content-Type-Options': 'nosniff'
        }

        if content_type:
            default_headers['Content-Type'] = content_type

        if extra_headers:
            default_headers.update(**extra_headers)

        response = {
            'isBase64Encoded': False,
            'statusCode': status_code,
            'body': data,
            'headers': default_headers
        }
        return response
