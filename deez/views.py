from deez.exceptions import ViewError


class View:
    """Base view"""

    def get_class_name(self) -> str:
        return self.__class__.__name__

    def __call__(self, method, *args, **kwargs):
        if not hasattr(self, method):
            raise ViewError(f'{method.upper()} method not implemented!')
        try:
            return getattr(self, method)(*args, **kwargs)
        except TypeError as e:
            raise ViewError(f'{self.get_class_name()}.{e.args[0]}')