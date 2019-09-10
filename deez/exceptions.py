class DeezError(RuntimeError):
    pass


class ResourceError(DeezError):
    pass


class NoResponseError(ResourceError):
    pass


class BadRequest400(ResourceError):
    pass


class NotAuthorized401(ResourceError):
    pass


class NotPermitted403(ResourceError):
    pass


class NotFound404(ResourceError):
    pass


class DuplicateRouteError(DeezError):
    pass


class TemplateNotFound(DeezError):
    pass