class DeezError(RuntimeError):
    pass


class ResourceError(DeezError):
    pass


class NoResponseError(ResourceError):
    pass


class NotFound404(ResourceError):
    pass


class DuplicateRouteError(DeezError):
    pass


class TemplateNotFound(DeezError):
    pass