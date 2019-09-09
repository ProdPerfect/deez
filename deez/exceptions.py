class DeezError(RuntimeError):
    pass


class ViewError(DeezError):
    pass


class NoResponseError(ViewError):
    pass


class NotFound404(ViewError):
    pass


class DuplicateRouteError(DeezError):
    pass


class TemplateNotFound(DeezError):
    pass