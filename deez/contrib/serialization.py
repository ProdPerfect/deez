from typing import Any, AnyStr

try:
    # prefer orjson over ujson if both are available
    import orjson as json
except ImportError:
    try:
        import ujson as json  # type: ignore
    except ImportError:
        import json  # type: ignore


def json_loads(s: AnyStr) -> Any:
    """

    :param s: JSON string to decode
    :type s: str
    :return: Decoded object
    :rtype:
    """
    return json.loads(s)


def json_dumps(obj: Any) -> Any:
    return json.dumps(obj)
