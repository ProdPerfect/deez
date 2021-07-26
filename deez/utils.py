import importlib
from typing import List, Union, Dict

from deez.middleware import Middleware


def import_resolver(module_path: str):
    """
    Takes a string reference to a class and returns
    an actual Python class.

    Example: "deez.middleware.Middleware"
    """
    split_path = module_path.split('.')
    attr = split_path[-1]
    package = '.'.join(split_path[:-1])
    module = importlib.import_module(package)
    return getattr(module, attr)


_invalid_middleware = "middleware %s is not a subclass of deez.middleware.Middleware"


def middleware_resolver(
        middleware_classes: List[Union[str, Dict[str, str]]]
) -> List[Middleware]:
    """
    Iteratively resolves middleware classes and returns a list of
    middleware instances to be used in Deez Router.
    """
    unsupported_type = "unsupported type %s used as middleware reference"
    middlewares = []
    for m in middleware_classes:
        assert isinstance(m, (str, dict)), unsupported_type % type(m)
        if isinstance(m, str):
            instance: Middleware = import_resolver(m)()
        else:
            instance: Middleware = import_resolver(m['middleware'])()
            setattr(instance, "path_regex", m['scope'])

        # for the time being, we're being strict about what actually is considered
        # a valid middleware class.
        assert isinstance(instance, Middleware), _invalid_middleware % instance.__class__.__name__

        middlewares.append(instance)

    return middlewares
