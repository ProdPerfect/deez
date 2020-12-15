class DeezError(RuntimeError):
    """Base Deez exception class"""


class ResourceError(DeezError):
    """Occurs when a resource method is not implemented"""


class NoResponseError(ResourceError):
    """Occurs when a resource does not return a response"""


class BadRequest(ResourceError):
    """Error to throw when the received payload is not as expected"""


class UnAuthorized(ResourceError):
    """Error to throw when a client is unauthorized to access this resource"""


class PermissionDenied(ResourceError):
    """Error to throw when a client is not permitted to access this resource"""


class NotFound(ResourceError):
    """This error is thrown when a resource is not found"""


class DuplicateRouteError(DeezError):
    """Thrown when a duplicate route is registered"""


class MethodNotAllowed(DeezError):
    """Thrown when a request is received with an unimplemented http verb"""
