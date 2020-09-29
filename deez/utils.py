import importlib
from typing import List, Type

from deez.middleware import Middleware


def import_resolver(module_path: str) -> Type[Middleware]:
    """
    Takes a string reference to a class and returns
    an actual Python class.

    Example: "deez.middlware.Middleware"
    """
    split_path = module_path.split('.')
    klass = split_path[-1]
    package = '.'.join(split_path[:-1])
    module = importlib.import_module(package)
    middleware_class = getattr(module, klass)
    assert issubclass(middleware_class, Middleware)
    return middleware_class


def resolve_middleware_classes(middleware_classes: List[str]) -> List[Type[Middleware]]:
    """
    Iteratively resolves middleware classes and returns a list of
    Python classes to be used in Deez Router.
    """
    return [import_resolver(m)
            for m in middleware_classes if m]
