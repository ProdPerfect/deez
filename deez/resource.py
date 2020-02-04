from deez.exceptions import ResourceError


class Resource:
    """Base Resource"""

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def __call__(self, method, *args, **kwargs):
        if not hasattr(self, method):
            raise ResourceError(f"{self.get_class_name()}'s '{method}' method not implemented!")
        try:
            return getattr(self, method)(*args, **kwargs)
        except TypeError as e:
            raise ResourceError(f'{self.get_class_name()}.{e.args[0]}')
