import os
import unittest
from unittest import mock


class SettingTestCase(unittest.TestCase):
    @mock.patch.dict(
        os.environ, {"PROJECT_SETTINGS_MODULE": "tests.settings"}, clear=True
    )
    def setUp(self, *args, **kwargs) -> None:
        from deez.conf import settings

        settings.configure()
        self.settings = settings

    def test_can_access_set_attributes(self):
        self.assertEqual(self.settings.DEBUG, True)

    def test_missing_attribute_does_not_trigger_max_recursion_error(self):
        with self.assertRaises(AttributeError) as e:
            self.assertEqual(self.settings.HAMZA, True)
        self.assertEqual(
            e.exception.args, ("'Setting' object has no attribute 'HAMZA'",)
        )
