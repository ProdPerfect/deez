from deez.request import Request
from deez.exceptions import ResourceError


class Resource:
    """
    Base Resource
    """

    def dispatch(self, *args, method: str = None, request: Request = None, **kwargs):
        """
        Tries to call the underlying user-implemented method that is responsible for
        serving the HTTP Method.
        """
        assert method is not None

        if not hasattr(self, method):
            raise ResourceError(f"{self._get_class_name()}'s '{method}' method not implemented!")
        try:
            return getattr(self, method)(request=request, *args, **kwargs)
        except TypeError as exc:
            raise ResourceError(f'{self._get_class_name()}.{exc.args[0]}')

    def _get_class_name(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return self._get_class_name()
