import re
from functools import lru_cache
from typing import Union

from deez.exceptions import BadRequest, DuplicateRouteError, NoResponseError, NotFound, PermissionDenied, UnAuthorized
from deez.request import Request
from deez.urls import Path


class Router:
    def __init__(self, app):
        self._app = app
        self._routes = {}
        self._route_names = {}
        self._route_patterns = []

    @lru_cache(maxsize=1000)
    def _get_re_match(self, path, method):
        matched_patterns = [
            pattern.search(path)
            for _, pattern in enumerate(self._route_patterns)
        ]

        if not matched_patterns:
            return None

        if len(matched_patterns) > 1:
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
                # TODO: Fix this later
                exact_pattern = self._routes.get(re_pattern)
                if exact_pattern:
                    best_pattern = best
                    break

                groups_len = len(best.groups())
                if groups_len > best_group_count:
                    best_pattern = best
                    best_group_count = groups_len
            return best_pattern
        else:
            return matched_patterns[0]

    def execute(self, event=None, context=None):
        request = Request(event, context=context)
        path = request.path
        method = request.http_method.lower()

        re_match = self._get_re_match(path=path, method=method)
        if not re_match:
            raise NotFound(f'{method.upper()} \'{path}\' not found!')

        resource_class = self._routes[re_match.re.pattern]()

        # middleware that needs to run before calling the resource
        middleware = self._app.middleware
        middleware_reversed = self._app.middleware_reversed

        for _, m in enumerate(middleware):
            _request = m(resource=resource_class).before_request(request=request)
            if _request:
                request = _request

        kwargs = re_match.groupdict()
        response = resource_class.dispatch(method=method, request=request, **kwargs)
        if not response:
            raise NoResponseError(f'{resource_class.get_class_name()} did not return a response')

        # middleware that needs to run before response
        for _, m in enumerate(middleware_reversed):
            _response = m(resource=resource_class).before_response(response=response)
            if _response:
                response = _response

        headers = response.headers
        status_code = 200
        content_type = response.content_type
        if hasattr(response, 'status_code'):
            status_code = response.status_code

        if hasattr(response, 'render'):
            return response.render(), status_code, headers, content_type
        return response, status_code, headers, content_type

    def _validate_path(self, path):
        if path in self._routes:
            raise DuplicateRouteError(f"\"{path}\" already defined")

    def register(self, path: Union[str, Path], resource=None):
        url_path = path
        url_resource = resource
        if isinstance(path, Path):
            url_path = path.regex
            url_resource = path.resource
        else:
            assert resource is not None

        self._validate_path(url_path)
        self._routes[url_path] = url_resource
        self._route_patterns.append(re.compile(url_path))

    def route(self, event, context):
        try:
            response, status_code, headers, content_type = self.execute(event=event, context=context)
            return self._make_response(status_code, response,
                                       content_type=content_type, extra_headers=headers)
        except BadRequest as e:
            return self._make_response(400, data=e.args[0])
        except UnAuthorized as e:
            return self._make_response(401, data=e.args[0])
        except PermissionDenied as e:
            return self._make_response(403, data=e.args[0])
        except NotFound as e:
            return self._make_response(404, data=e.args[0])

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
