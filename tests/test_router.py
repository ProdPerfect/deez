from typing import Type
from uuid import uuid4

import pytest

from deez import Deez
from deez.contrib.serialization import json_dumps
from deez.resource import Resource
from deez.response import JsonResponse
from deez.urls import path

from .mock_event import event_v1


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
        ("/hello/world", "/hello/world", "get", True),
    ],
)
def test_find_route_match(route, request_path, method, found) -> None:
    app = Deez()
    app.register_route(
        path(route, _make_resource()),
    )
    assert bool(app.router.find_route_match(request_path, method)) == found


def test_execute_returns_expected_response() -> None:
    app = Deez()
    app.register_route(
        path("/hello/world", _make_resource()),
    )
    response = app.process_request(event_v1, {})
    assert response["statusCode"] == 200
    assert response["body"] == json_dumps({"foo": "bar"})
