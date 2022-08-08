from typing import Pattern, Optional


class Middleware:
    """
    base class for implementing middleware
    """

    def __init__(self, path_regex: Optional[Pattern] = None) -> None:
        self.path_regex = path_regex



    def run(self, path: str) -> bool:
        """function that checks wether a middleware's 
        before_request and after_request methods should be called.
        """
        return not self.path_regex or bool(self.path_regex.match(path))
