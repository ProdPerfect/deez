import asyncio
from typing import Callable

from deez.conf import settings
from deez.exceptions import MethodNotAllowed
from deez.request import Request
from deez.response import JsonResponse

_HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


class Resource:
    """
    Base API Resource
    """

    def _get_allowed_methods(self) -> str:
        methods = ["OPTIONS"]
        for m in _HTTP_METHODS:
            if hasattr(self, m):
                methods.append(m.upper())
        return ", ".join(methods)

    def head(self, request, *args, **kwargs) -> JsonResponse:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD

        func: Callable = getattr(self, "get")
        if func is None:
            return JsonResponse(data={}, status_code=405)

        if asyncio.iscoroutinefunction(func):
            response = asyncio.run(func(request, *args, **kwargs))
        else:
            response = func(request, *args, **kwargs)
        response.data = {}
        response.headers["Content-Length"] = "0"
        return response

    def options(self, request, *args, **kwargs) -> JsonResponse:
        headers = {
            "Access-Control-Max-Age": settings.ACCESS_CONTROL_MAX_AGE,
            "Access-Control-Allow-Origin": settings.ACCESS_CONTROL_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": self._get_allowed_methods(),
        }
        return JsonResponse(data={}, status_code=204, headers=headers)

    def dispatch(self, request: Request, **kwargs) -> JsonResponse:
        """
        Tries to call the underlying user-implemented method that is responsible for
        serving the HTTP Method.
        """
        method: str = request.method.lower()
        if not hasattr(self, method):
            raise MethodNotAllowed("method not allowed!")

        func: Callable[..., JsonResponse] = getattr(self, method)
        # add experimental support for async functions
        if asyncio.iscoroutinefunction(func):
            return asyncio.run(func(request=request, **kwargs))
        return func(request=request, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__
