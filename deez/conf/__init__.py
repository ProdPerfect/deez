import importlib
import os
from typing import Iterable

from deez.conf import default_settings
from deez.functional import SimpleLazyObject


def load_settings_module():
    settings_module = os.environ['PROJECT_SETTINGS_MODULE']
    setting = importlib.import_module(settings_module)
    return setting


class Setting:
    def __init__(self):
        self._loaded = False

    def _setup(self):
        for setting in dir(default_settings):
            setattr(self, setting, getattr(default_settings, setting))

        imp = load_settings_module()
        for setting in dir(imp):
            setattr(self, setting, getattr(imp, setting))

    def __dir__(self) -> Iterable[str]:
        return [k for k in self.__dict__.keys() if k.isupper()]

    def __getattr__(self, item):
        if not self._loaded:
            self._setup()
            self._loaded = True
        return getattr(self, item)


settings = SimpleLazyObject(lambda: Setting())