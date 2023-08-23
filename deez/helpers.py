from typing import Any


def method_proxy(cls: Any, attr: str) -> Any:
    return object.__getattribute__(cls, attr)
