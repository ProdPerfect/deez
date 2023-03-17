from typing import Type, Optional

from deez.resource import Resource
from deez.urls.parsers import pattern_replacer


class Path:
    def __init__(
        self, regex: str, resource: Type[Resource], raw_url: Optional[str] = None
    ):
        self.regex = regex
        self.raw_url = raw_url
        self.resource = resource


def path(url: str, resource: Type[Resource]) -> Path:
    regex = pattern_replacer(url)
    return Path(regex, resource, raw_url=url)


__all__ = ["Path", "path"]
