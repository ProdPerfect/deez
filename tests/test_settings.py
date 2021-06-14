import os
import unittest


class SettingTestCase(unittest.TestCase):
    def setUp(self, *args, **kwargs) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')

    def test_can_access_set_attributes(self):
        from deez.conf import settings
        self.assertEqual(settings.DEBUG, True)

    def test_missing_attribute_does_not_trigger_max_recursion_error(self):
        from deez.conf import settings
        with self.assertRaises(AttributeError) as e:
            self.assertEqual(settings.HAMZA, True)
        self.assertEqual(e.exception.args, ("'Setting' object has no attribute 'HAMZA'",))
