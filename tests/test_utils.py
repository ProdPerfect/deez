import re
import unittest

from deez.utils import middleware_resolver


class UtilityFunctionTestCases(unittest.TestCase):

    def test_resolve_default_middleware(self):
        refs = ['tests.middleware.TestMiddleware']
        resolved_refs = middleware_resolver(refs)
        self.assertTrue(len(resolved_refs) == 1)
        self.assertFalse(resolved_refs[0].is_scoped)

    def test_resolve_scoped_middleware(self):
        refs = [
            {
                'middleware': 'tests.middleware.TestMiddleware',
                'scope': re.compile(r"/hello/world")
            },
        ]
        resolved_refs = middleware_resolver(refs)
        self.assertTrue(len(resolved_refs) == 1)
        self.assertTrue(resolved_refs[0].is_scoped)
