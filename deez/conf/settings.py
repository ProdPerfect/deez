import importlib
import os
from types import ModuleType
from typing import Any, Dict, List, Union

from deez.conf import default_settings
from deez.core.signals import settings_configured
from deez.helpers import method_proxy


def import_settings_module() -> ModuleType:
    _settings_module = os.getenv("PROJECT_SETTINGS_MODULE")
    assert _settings_module is not None, (
        "You must set PROJECT_SETTINGS_MODULE "
        "as an environment variable with a path to "
        "you settings module."
    )
    setting = importlib.import_module(_settings_module)
    return setting


class Setting:
    DEBUG: bool
    MIDDLEWARE: List[Union[str, Dict[str, str]]]
    EXCEPTION_HANDLER: str
    ACCESS_CONTROL_MAX_AGE: int
    ACCESS_CONTROL_ALLOW_ORIGIN: str

    def __init__(self) -> None:
        self._loaded = False
        self._configured = False
        self._extended = {}

    def _set_default_settings(self) -> None:
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

    def _set_user_settings(self) -> None:
        imp = import_settings_module()
        for setting in dir(imp):
            if setting.isupper():
                setattr(self, setting, getattr(imp, setting))

    def configure(self) -> None:
        # skip setting attributes again if we've done it before
        if self._configured:
            pass
        else:
            self._set_default_settings()
            self._set_user_settings()
            # only after `configured` is set to true can the settings object be used
            self._configured = True

        settings_configured.send(self)

    def __getattr__(self, item) -> Any:
        if not self._configured:
            raise RuntimeError(
                "Settings have not yet been configured. "
                "You must call Setting.configure() before settings can be used."
            )
        return method_proxy(self, item)

    def extend(self, *, configurations: Dict[str, Any]) -> None:
        """Note: experimental!!"""
        for k, v in configurations.items():
            setattr(self, k, v)
