from typing import AnyStr, Union, List, Any, Dict

try:
    import ujson as json
except ImportError:
    import json


def json_loads(s: AnyStr) -> Union[List[Any], Dict[str, Any]]:
    """

    :param s: JSON string to decode
    :type s: str
    :return: Decoded object
    :rtype:
    """
    return json.loads(s)


def json_dumps(obj: Any) -> str:
    return json.dumps(obj)
