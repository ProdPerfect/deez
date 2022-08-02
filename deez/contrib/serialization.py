from typing import Union, List, Dict, AnyStr

try:
    import ujson as json
except ImportError:
    import json  # type: ignore


def json_loads(s: AnyStr) -> Union[List, Dict, str, int]:
    """

    :param s: JSON string to decode
    :type s: str
    :return: Decoded object
    :rtype:
    """
    return json.loads(s)


def json_dumps(obj: Union[List, Dict, str, int]) -> str:
    return json.dumps(obj)
