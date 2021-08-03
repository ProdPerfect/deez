import importlib
import os
from typing import Any, Dict, List, Union, Pattern

from deez.conf import default_settings

_missing_settings_module_message = (
    "You must set PROJECT_SETTINGS_MODULE "
    "as an environment variable with a path to you settings module.")


def proxy_method(cls, attr: str) -> Any:
    return object.__getattribute__(cls, attr)


class Setting:
    DEBUG: bool
    MIDDLEWARE: List[Union[str, Dict[str, str]]]
    CAMELCASE_REGEX: Pattern
    EXCEPTION_HANDLER: str
    LOGGER_MESSAGE_FORMAT: str

    def __init__(self) -> None:
        self._loaded: bool = False
        self._extended: Dict[str, Any] = {}

    def load_module(self) -> Any:
        ref = os.getenv('PROJECT_SETTINGS_MODULE')
        assert ref is not None, _missing_settings_module_message
        return importlib.import_module(ref)

    def _setup(self) -> None:
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        imp = self.load_module()
        for setting in dir(imp):
            setattr(self, setting, getattr(imp, setting))

    def __getattr__(self, key: str) -> Any:
        if not self._loaded:
            self._setup()
            self._loaded = True
        return proxy_method(self, key)

    def _reload(self) -> None:
        # only used for debugging purposes
        self._setup()

    def extend(self, *, configurations: Dict[str, Any]) -> None:
        """Note: experimental!!
        """
        for k, v in configurations.items():
            self._extended = configurations
            setattr(self, k, v)


settings = Setting()
