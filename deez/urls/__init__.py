from deez.urls.parsers import pattern_replacer


class Path:
    def __init__(self, regex, resource, raw_url=None):
        self.regex = regex
        self.raw_url = raw_url
        self.resource = resource


def path(url, resource) -> Path:
    regex = pattern_replacer(url)
    return Path(regex, resource, raw_url=url)


__all__ = [Path, path]
