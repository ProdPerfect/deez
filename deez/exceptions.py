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


class Forbidden(ResourceError):
    """Error to throw when a client is not permitted to access this resource"""


class NotFound(ResourceError):
    """This error is thrown when a resource is not found"""


class DuplicateRouteError(DeezError):
    """Thrown when a duplicate route is registered"""


class MethodNotAllowed(DeezError):
    """Thrown when a request is received with an unimplemented http verb"""


class UnsupportedMediaType(DeezError):
    """The media format of the requested data is not supported by the server, so the server is rejecting the request."""


class TooManyRequests(DeezError):
    """The user has sent too many requests in a given amount of time ("rate limiting")."""
