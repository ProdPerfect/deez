from deez.urls.parsers import pattern_replacer


class Path:
    def __init__(self, regex, resource):
        self.regex = regex
        self.resource = resource


def path_resolver(url: str, resource) -> Path:
    regex = pattern_replacer(url)
    return Path(regex, resource)


__all__ = ['Path', 'path_resolver']
