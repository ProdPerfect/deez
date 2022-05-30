from deez.exceptions import MethodNotAllowed


class Resource:
    """
    Base API Resource
    """

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
