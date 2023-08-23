from typing import Any


def method_proxy(cls, attr: str) -> Any:
    return object.__getattribute__(cls, attr)
