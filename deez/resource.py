from deez.exceptions import MethodNotAllowed
from deez.response import JsonResponse
from deez.conf import settings

_HTTP_METHODS = {'get', 'post', 'put', 'patch', 'delete'}


class Resource:
    """
    Base API Resource
    """

    def _get_methods(self) -> str:
        methods = ['OPTIONS']
        for m in _HTTP_METHODS:
            if hasattr(self, m):
                methods.append(m.upper())
        return ', '.join(methods)

    def head(self, request, *args, **kwargs):
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD
        response = self.get(request, *args, **kwargs)
        response.data = {}
        return response

    def options(self, request, *args, **kwargs) -> JsonResponse:
        headers = {
            'Access-Control-Max-Age': settings.ACCESS_CONTROL_MAX_AGE,
            'Access-Control-Allow-Origin': settings.ACCESS_CONTROL_ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': self._get_methods(),
        }
        return JsonResponse(data={}, status_code=204, headers=headers)

    def dispatch(self, request=None, **kwargs):
        """
        Tries to call the underlying user-implemented method that is responsible for
        serving the HTTP Method.
        """
        method = request.method.lower()
        if not hasattr(self, method):
            raise MethodNotAllowed("method not allowed!")
        return getattr(self, method)(request=request, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__
