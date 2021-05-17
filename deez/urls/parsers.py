import re

from typing import Dict, List

# RFC 4122 states that the characters should be output as lowercase, but
# that input is case-insensitive. When validating input strings,
# include re.I or re.IGNORECASE per below:

_UUID4_PATTERN = r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
_PATTERN_DETECTOR = re.compile(r"(<.*?>)", re.IGNORECASE)
_ALIAS_TO_REGEX: Dict[str, str] = {
    'int': r'\d+',
    'str': r'[a-zA-Z0-9-_]+',
    'slug': r'[-\w]+',
    'uuid': _UUID4_PATTERN,
    'number': r'\d*[.,]?\d+',
}


def register_alias(alias: str, regex: str) -> None:
    """
    Register a new alias to be used in application urls

    ex:
        register_alias('jira', r'DG-[0-9]{3}')
        path('/ticket/<jira:id>')
    """
    _ALIAS_TO_REGEX[alias] = regex


def find_patterns(value: str) -> List[str]:
    """
    Finds all <alias:name> parameters in a URL
    """
    return _PATTERN_DETECTOR.findall(value)


def pattern_replacer(string: str) -> str:
    """
    Converts <alias:name> to named regex groups
    """
    if string.startswith('/'):
        string = string[1:]

    original_url = string
    patterns = find_patterns(original_url)
    for pattern in patterns:
        if ':' not in pattern:
            continue
        alias, name = re.sub(r"[^a-z_:]", '', pattern).split(':', maxsplit=1)
        named_pattern = '(?P<%s>%s)' % (name, _ALIAS_TO_REGEX[alias])
        original_url = original_url.replace(pattern, named_pattern)

    cleaned_url = r'^/%s$' % original_url
    return cleaned_url
