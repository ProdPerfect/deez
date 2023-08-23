import re

from deez.utils import middleware_resolver


def test_resolve_default_middleware():
    refs = ["tests.middleware.TestMiddleware"]
    resolved_refs = middleware_resolver(refs)
    assert len(resolved_refs) == 1


def test_resolve_scoped_middleware():
    refs = [
        {
            "middleware": "tests.middleware.TestMiddleware",
            "scope": re.compile(r"/hello/world"),
        },
    ]
    resolved_refs = middleware_resolver(refs)
    assert len(resolved_refs) == 1
