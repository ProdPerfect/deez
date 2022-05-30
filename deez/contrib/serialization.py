from typing import Any

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


def json_loads(s: Any) -> Any:
    """

    :param s: JSON string to decode
    :type s: str
    :return: Decoded object
    :rtype:
    """
    return json.loads(s)


def json_dumps(obj: Any) -> str:
    return json.dumps(obj)
