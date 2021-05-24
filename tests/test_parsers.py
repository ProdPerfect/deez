import unittest

from deez.urls.parsers import pattern_replacer, register_alias


class ParseTestCase(unittest.TestCase):

    def test_pattern_replacer_int(self):
        url = pattern_replacer("users/<int:name>/")
        self.assertEqual(r"^/users/(?P<name>\d+)/$", url)

    def test_pattern_replacer_str(self):
        url = pattern_replacer("users/<str:name>/")
        self.assertEqual(r"^/users/(?P<name>[a-zA-Z0-9-_]+)/$", url)

    def test_pattern_replacer_slug(self):
        url = pattern_replacer("users/<slug:username>/")
        self.assertEqual(r"^/users/(?P<username>[-\w]+)/$", url)

    def test_pattern_replacer_number(self):
        url = pattern_replacer("users/<number:id>/")
        self.assertEqual(r"^/users/(?P<id>\d*[.,]?\d+)/$", url)

    def test_pattern_replacer_uuid(self):
        url = pattern_replacer("users/<uuid:name>/")
        self.assertEqual(
            r"^/users/(?P<name>[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$", url)

    def test_register_alias(self):
        register_alias('jira', r'DG-[0-3]{3}')

        url = pattern_replacer('tickets/<jira:id>/')
        self.assertEqual(r"^/tickets/(?P<id>DG-[0-3]{3})/$", url)
