from deez.conf import Setting
from deez.router import Router
from deez.utils import resolve_middleware_classes


class Deez:
    def __init__(self) -> None:
        self.router: Router
        self.settings: Setting
        self.middleware = []
        self.middleware_reversed = []

        self._setup()

    def _setup(self) -> None:
        from deez.conf import settings

        self.settings = settings
        self.router = Router(self)
        if hasattr(self.settings, 'MIDDLEWARE'):
            self.middleware = resolve_middleware_classes(self.settings.MIDDLEWARE)
            self.middleware_reversed = reversed(self.middleware)

    def register_route(self, path, resource_class=None) -> None:
        self.router.register(path=path, resource=resource_class)

    def process_request(self, event, context):
        return self.router.route(event, context)
