import re
from functools import lru_cache
from typing import Any, Dict, Match, Optional

from deez.exceptions import BadRequest400, DuplicateRouteError, NoResponseError, NotAuthorized401, NotFound404, \
    NotPermitted403
from deez.request import Request


class Router:
    def __init__(self, app):
        self._app = app
        self._routes = {}
        self._route_names = {}
        self._route_patterns = []

    @lru_cache(maxsize=100)
    def _get_re_match(self, path: str, method: str) -> Optional[Match]:
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

            # method required to serve this request was not implemented
            if not best_match:
                return None

            best_pattern = None
            best_group_count = 0

            for _, best in enumerate(best_match):
                groups_len = len(best.groups())
                if groups_len > best_group_count:
                    best_pattern = best
                    best_group_count = groups_len
            return best_pattern
        else:
            return matched_patterns[0]

    def execute(self, event=None, context=None) -> Any:
        request = Request(event, context=context)
        path = request.path
        method = request.http_method.lower()

        re_match = self._get_re_match(path=path, method=method)
        if not re_match:
            raise NotFound404(f'{method.upper()} \'{path}\' not found!')

        resource_class = self._routes[re_match.re.pattern]()

        # middleware that needs to run before calling the resource
        middleware = self._app.middleware

        for _, m in enumerate(middleware):
            _request = m(resource=resource_class).before_request(request=request)
            if _request:
                request = _request

        kwargs = re_match.groupdict()
        response = resource_class(method, request, **kwargs)
        if not response:
            raise NoResponseError(f'{resource_class.get_class_name()} did not return anything')

        # middleware that needs to run before response
        for _, m in enumerate(reversed(middleware)):
            _response = m(resource=resource_class).before_response(response=response)
            if _response:
                response = _response

        if hasattr(response, 'render'):
            return response.render(self._app.template_loader)
        return response

    def _validate_path(self, path: str) -> None:
        if path in self._routes:
            raise DuplicateRouteError(f"\"{path}\" already defined")

    def register(self, path: str, resource) -> None:
        self._validate_path(path)
        self._routes[path] = resource
        self._route_patterns.append(re.compile(path))

    def route(self, event: Dict, context: object) -> Any:
        try:
            return self.execute(event=event, context=context)
        except BadRequest400 as e:
            return self._make_response(400, data=e.args[0])
        except NotAuthorized401 as e:
            return self._make_response(401, data=e.args[0])
        except NotPermitted403 as e:
            return self._make_response(403, data=e.args[0])
        except NotFound404 as e:
            return self._make_response(404, data=e.args[0])

    def _make_response(self, status_code, data, content_type='application/json'):
        return {
            'isBase64Encoded': False,
            'statusCode': status_code,
            'body': data,
            'headers': {
                'Content-Type': content_type,
                'Access-Control-Allow-Origin': '*'
            }
        }