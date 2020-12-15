from deez.exceptions import MethodNotAllowed


class Resource:
    """
    Base Resource
    """

    def dispatch(self, method=None, request=None, **kwargs):
        """
        Tries to call the underlying user-implemented method that is responsible for
        serving the HTTP Method.
        """
        assert method is not None

        if not hasattr(self, method):
            raise MethodNotAllowed("method not allowed!")
        return getattr(self, method)(request=request, **kwargs)

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self.get_class_name()
