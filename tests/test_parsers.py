import unittest

from deez.urls.parsers import pattern_replacer


class ParseTestCase(unittest.TestCase):

    def test_pattern_replacer_int(self):
        url = pattern_replacer("users/<int:name>/")
        self.assertEqual(r"^/users/(?P<name>)\d+/$", url)

    def test_pattern_replacer_str(self):
        url = pattern_replacer("users/<str:name>/")
        self.assertEqual(r"^/users/(?P<name>)[a-zA-Z0-9-_]+/$", url)

    def test_pattern_replacer_uuid(self):
        url = pattern_replacer("users/<uuid:name>/")
        self.assertEqual(
            r"^/users/(?P<name>)[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/$", url)
