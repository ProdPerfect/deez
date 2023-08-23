import re
from unittest import mock

from deez.conf import settings
from deez.deez import Deez
from deez.middleware import Middleware
from deez.resource import Resource
from deez.response import JsonResponse
from deez.urls import path
from tests.mock_event import event_v1


class HelloWorldResource(Resource):
    def get(self, request, *args, **kwargs) -> JsonResponse:
        return JsonResponse(data={"message": "hello world", "user": request.user.as_dict()})


@mock.patch.object(settings, "MIDDLEWARE", ["tests.middleware.TestMiddleware"])
def test_modifies_response() -> None:
    app = Deez()
    app.register_route(path("/hello/world", HelloWorldResource))
    response = app.router.route(event_v1, {})
    assert response, {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": b'{"statusCode":200,"message":"hello world","user":{"name":"Lemi","age":1000000}}',
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Content-Type-Options": "nosniff",
        },
    }


def test_scoped_middleware_run_when_path_regex_and_route_match() -> None:
    class TestScopedMiddleware(Middleware):
        pass

    m = TestScopedMiddleware(path_regex=re.compile(r"/hello/world"))
    assert m.run("/hello/world") == True


def test_scoped_middleware_does_not_run_when_path_regex_and_route_mismatched() -> None:
    class TestScopedMiddleware(Middleware):
        pass

    m = TestScopedMiddleware(path_regex=re.compile(r"/hello/world"))
    assert m.run("/hella/weird") == False
