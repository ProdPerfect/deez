from functools import lru_cache
from re import Pattern


class Middleware:
    """default base middleware implementation
    """
    scoped: bool = False

    def before_request(self, request):
        return request

    def before_response(self, response):
        return response

    @classmethod
    def run(cls, path: str) -> bool:
        return True


_invalid_regex = """`path_regex` should be a valid compiled regex pattern"""


class ScopedMiddleware(Middleware):
    """
    middleware that can be scoped to only run on a request path match.
    """
    scoped: bool = True
    path_regex: Pattern = None

    @classmethod
    @lru_cache()
    def run(cls, path: str) -> bool:
        assert isinstance(cls.path_regex, Pattern), _invalid_regex
        return cls.scoped and cls.path_regex.match(path)
