from deez.conf import settings
from deez.router import Router
from deez.utils import resolve_middleware_classes


class Deez:
    def __init__(self):
        self.router = None
        self._setup()

    def _setup(self):
        self.settings = settings
        self.router = Router(self)

        middleware = settings.MIDDLEWARE
        if not middleware:
            middleware = []

        self.middleware = resolve_middleware_classes(middleware)

    def register_route(self, path: str, resource_class):
        self.router.register(path=path, resource=resource_class)

    def process_request(self, event, context):
        return self.router.route(event, context)