from typing import Type
from uuid import uuid4

import pytest

from deez import Deez
from deez.resource import Resource
from deez.response import JsonResponse
from deez.urls import path


def _make_resource() -> Type[Resource]:
    class DynamicResource(Resource):
        def get(self, request, *args, **kwargs) -> JsonResponse:
            return JsonResponse({"foo": "bar"})

    return DynamicResource


@pytest.mark.parametrize(
    "route,request_path,method,found",
    [
        ("/", "/", "get", True),
        ("/foo/<int:hello>", "/foo", "get", False),
        ("/foo/<int:hello>", "/foo/123", "get", True),
        ("/foo/<int:hello>", "/foo/hello", "post", False),
        ("/foo/<int:hello>", "/foo/123.00", "post", False),
        ("/foo/<number:hello>", "/foo/123.00", "get", True),
        ("/foo/<uuid:hello>", f"/foo/{uuid4()}", "get", True),
    ],
)
def test_find_route_match(route, request_path, method, found) -> None:
    app = Deez()
    app.register_route(
        path(route, _make_resource()),
    )
    assert bool(app.router.find_route_match(request_path, method)) == found
