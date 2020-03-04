from deez import Request
from deez.exceptions import ResourceError


class Resource:
    """
    Base Resource
    """

    def dispatch(self, method: str = None, request: Request = None, *args, **kwargs):
        if not hasattr(self, method):
            raise ResourceError(f"{self.get_class_name()}'s '{method}' method not implemented!")
        try:
            return getattr(self, method)(request=request, *args, **kwargs)
        except TypeError as e:
            raise ResourceError(f'{self.get_class_name()}.{e.args[0]}')

    def get_class_name(self):
        return self.__class__.__name__

    def __str__(self):
        return self.get_class_name()
