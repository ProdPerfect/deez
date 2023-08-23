import re
from typing import Dict, List

_UUID4_PATTERN = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
_PATTERN_DETECTOR = re.compile(r"(<.*?>)", re.IGNORECASE)
_ALIAS_TO_REGEX: Dict[str, str] = {
    "int": r"\d+",
    "str": r"[a-zA-Z0-9-_]+",
    "slug": r"[-\w]+",
    "uuid": _UUID4_PATTERN,
    "number": r"\d*[.,]?\d+",
}

_RESERVED_ALIAS_NAMES = {"int", "str", "slug", "uuid", "number"}


def register_alias(alias: str, regex: str) -> None:
    """
    Register a new alias to be used in application urls

    ex:
        register_alias('jira', r'DG-[0-9]{3}')
        path('/ticket/<jira:id>')
    """

    if alias in _ALIAS_TO_REGEX:
        raise ValueError("alias %s already registered" % alias)
    elif alias in _RESERVED_ALIAS_NAMES:
        raise ValueError("alias %s is reserved" % alias)

    _ALIAS_TO_REGEX[alias] = regex


def find_patterns(value: str) -> List[str]:
    """
    Finds all <alias:name> parameters in a URL
    """
    return _PATTERN_DETECTOR.findall(value)


def alias_translator(string: str) -> str:
    """
    Converts <alias:name> to named regex groups
    """
    if string.startswith("/"):
        string = string[1:]

    original_url = string
    patterns = find_patterns(original_url)
    for pattern in patterns:
        if ":" not in pattern:
            continue
        alias, name = re.sub(r"[^a-z_:]", "", pattern).split(":", maxsplit=1)
        named_pattern = "(?P<%s>%s)" % (name, _ALIAS_TO_REGEX[alias])
        original_url = original_url.replace(pattern, named_pattern)

    cleaned_url = r"^/%s$" % original_url
    return cleaned_url
