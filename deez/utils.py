import importlib
from typing import List, Type
from deez.middleware import Middleware


def import_resolver(module_path: str) -> Type[Middleware]:
    """
    Takes a string reference to a class and turns it into
    an actual Python class.

    Example: "deez.middlware.Middleware"
    """
    path = module_path.split('.')
    name = '.'.join(path[:-1])
    package = path[-1:][0]
    module = importlib.import_module(name, package=package)
    return getattr(module, package)


def resolve_middleware_classes(middleware_classes: List[str]) -> List[Type[Middleware]]:
    """
    Iteratively resolves middleware classes and returns a list of
    Python classes to be used in Deez Router.
    """
    return [import_resolver(m)
            for m in middleware_classes if m]
