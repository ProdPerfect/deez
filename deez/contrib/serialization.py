from typing import Any, Union

try:
    import ujson as json  # type: ignore
except ImportError:
    import json  # type: ignore


def json_loads(s: Union[bytes, str, bytearray]) -> Any:
    """

    :param s: JSON string to decode
    :type s: str
    :return: Decoded object
    :rtype:
    """
    return json.loads(s)


def json_dumps(obj: Any) -> bytes:
    return json.dumps(obj).encode("utf-8")
