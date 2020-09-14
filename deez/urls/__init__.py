from deez.logger import get_logger
from deez.urls.parsers import pattern_replacer


class Path:
    def __init__(self, regex, resource):
        self.regex = regex
        self.resource = resource


def path(url: str, resource) -> Path:
    regex = pattern_replacer(url)
    return Path(regex, resource)


def path_resolver(url: str, resource) -> Path:
    """
    Will be deprecated in favor of `path` in
    future versions.
    """
    logger = get_logger()
    logger.warning("use path instead of path_resolver: %s", url)
    return path(url, resource)


__all__ = [Path, path, path_resolver]
