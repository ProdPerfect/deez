from typing import Any


def method_proxy(cls, attr) -> Any:
    return object.__getattribute__(cls, attr)
