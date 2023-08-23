import os

import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(items):
    os.environ["PROJECT_SETTINGS_MODULE"] = "tests.settings"
    from deez.conf import settings

    settings.configure()
    outcome = yield
