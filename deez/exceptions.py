class DeezError(RuntimeError):
    pass


class ResourceError(DeezError):
    pass


class NoResponseError(ResourceError):
    pass


class BadRequest(ResourceError):
    pass


class UnAuthorized(ResourceError):
    pass


class PermissionDenied(ResourceError):
    pass


class NotFound(ResourceError):
    pass


class DuplicateRouteError(DeezError):
    pass


class TemplateNotFound(DeezError):
    pass
