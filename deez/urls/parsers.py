import re

from typing import List

# RFC 4122 states that the characters should be output as lowercase, but
# that input is case-insensitive. When validating input strings,
# include re.I or re.IGNORECASE per below:

UUID4_PATTERN = r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
PATTERN_DETECTOR = re.compile(r"(<.*?>)", re.IGNORECASE)

_alias_to_regex = {
    'int': r'\d+',
    'str': r'\w+',
    'uuid': UUID4_PATTERN,
}


def find_patterns(value: str) -> List[str]:
    return PATTERN_DETECTOR.findall(value)


def pattern_replacer(string: str) -> str:
    if string.startswith('/'):
        string = string[1:]

    original_url = string
    patterns = find_patterns(original_url)
    for pattern in patterns:
        if ':' not in pattern:
            continue
        alias, name = re.sub(r"[^a-z:]", '', pattern).split(':', maxsplit=1)
        named_pattern = '(?P<%s>)%s' % (name, _alias_to_regex[alias])
        original_url = original_url.replace(pattern, named_pattern)

    cleaned_url = r'^/%s$' % original_url
    return cleaned_url
