import importlib
from typing import Any, List, Union, Dict

from deez.middleware import Middleware


def import_string(module_path: str) -> Any:
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


_INVALID_MIDDLEWARE_MESSAGE = "%s is not a subclass of deez.middleware.Middleware"


def middleware_resolver(
        middleware_classes: List[Union[str, Dict[str, str]]]
) -> List[Middleware]:
    """
    Iteratively resolves middleware classes and returns a list of
    middleware instances to be used in Deez Router.
    """
    unsupported_type = "middleware references must be of type string or dict, not %s"
    middlewares: List[Middleware] = []
    for klass in middleware_classes:
        instance: Middleware
        assert isinstance(klass, (str, dict)), unsupported_type % type(klass)
        if isinstance(klass, str):
            instance = import_string(klass)()
        else:
            instance = import_string(klass['middleware'])(path_regex=klass['scope'])

        # for the time being, we're being strict about what actually is considered
        # a valid middleware class.
        assert isinstance(instance, Middleware), _INVALID_MIDDLEWARE_MESSAGE % instance.__class__.__name__

        middlewares.append(instance)

    return middlewares
