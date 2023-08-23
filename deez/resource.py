import asyncio
import sys
from typing import Callable

from deez.conf import settings
from deez.exceptions import MethodNotAllowed
from deez.request import Request
from deez.response import JsonResponse

_HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}


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

    async def head(self, request, **kwargs) -> JsonResponse:
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD
        func: Callable = getattr(self, "get")
        if func is None:
            return JsonResponse(data={}, status_code=405)

        if asyncio.iscoroutinefunction(func):
            response = asyncio.run(func(request, **kwargs))
        else:
            response = func(request, **kwargs)
        response.data = {}
        response.headers["Content-Length"] = sys.getsizeof(response.data)
        return response

    async def options(self, request, **kwargs) -> JsonResponse:
        headers = {
            "Access-Control-Max-Age": settings.ACCESS_CONTROL_MAX_AGE,
            "Access-Control-Allow-Origin": settings.ACCESS_CONTROL_ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": self._get_allowed_methods(),
        }
        return JsonResponse(data={}, status_code=204, headers=headers)

    async def dispatch(self, request: Request, **kwargs) -> JsonResponse:
        """
        Tries to call the underlying user-implemented method that is responsible for
        serving the HTTP Method.
        """
        method: str = request.method.lower()
        if not hasattr(self, method):
            raise MethodNotAllowed("method not allowed!")

        func: Callable[..., JsonResponse] = getattr(self, method)
        if asyncio.iscoroutinefunction(func):
            return await func(request=request, **kwargs)
        return func(request=request, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__
