import os
import re
import unittest
from unittest import mock

from deez.conf import settings
from deez.deez import Deez
from deez.middleware import Middleware
from deez.resource import Resource
from deez.response import JsonResponse
from deez.urls import path
from tests.mock_event import event


class HelloWorldResource(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world', 'user': request.user.as_dict()})


class MiddlewareTestCase(unittest.TestCase):

    @mock.patch.dict(os.environ, {'PROJECT_SETTINGS_MODULE': 'tests.settings'}, clear=True)
    def setUp(self, *args, **kwargs) -> None:
        from deez.conf import settings
        settings.configure()

    @mock.patch.object(settings, 'MIDDLEWARE', ['tests.middleware.TestMiddleware'])
    def test_modifies_response(self):
        app = Deez()
        app.register_route(path('/hello/world', HelloWorldResource))
        response = app.router.route(event, {})
        self.assertEqual(
            response,
            {
                'isBase64Encoded': False, 'statusCode': 200,
                'body': '{"statusCode":200,"message":"hello world","user":{"name":"Lemi","age":1000000}}',
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'X-Content-Type-Options': 'nosniff'
                }
            }
        )

    def test_scoped_middleware(self):
        class TestScopedMiddleware(Middleware):
            pass

        m = TestScopedMiddleware(path_regex=re.compile(r"/hello/world"))
        # runs when path_regex matches request path
        self.assertTrue(m.run("/hello/world"))
        # does not run when path_regex does not match request path
        self.assertFalse(m.run("/hella/weird"))
