import importlib
import os

from deez.conf import default_settings


def load_settings_module():
    settings_module = os.getenv('PROJECT_SETTINGS_MODULE')
    assert settings_module is not None, "You must set PROJECT_SETTINGS_MODULE " \
                                        "as an environment variable with a path to " \
                                        "you settings module."
    setting = importlib.import_module(settings_module)
    return setting


def proxy_method(cls, attr):
    return object.__getattribute__(cls, attr)


class Setting:
    def __init__(self):
        self._loaded = False

    def _setup(self):
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        imp = load_settings_module()
        for setting in dir(imp):
            setattr(self, setting, getattr(imp, setting))

    def __getattr__(self, item):
        if not self._loaded:
            self._setup()
            self._loaded = True
        return proxy_method(self, item)

    def _reload(self):
        # only used for debugging purposes
        self._setup()


settings = Setting()
