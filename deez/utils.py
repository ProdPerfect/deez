import importlib


def import_resolver(module_path):
    path = module_path.split('.')
    name = '.'.join(path[:-1])
    package = path[-1:][0]
    module = importlib.import_module(name, package=package)
    return getattr(module, package)


def resolve_middleware_classes(middleware_classes):
    return [import_resolver(m)
            for m in middleware_classes]
