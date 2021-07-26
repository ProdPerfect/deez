import os
import re
import unittest
from unittest import mock

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

    def test_can_route_correctly(self):
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'tests.settings')
        with mock.patch('tests.settings.MIDDLEWARE', ['tests.middleware.TestMiddleware']):
            app = Deez()
            app.register_route(path('/hello/world', HelloWorldResource))
            response = app.router.route(event, {})
            self.assertEqual(
                response,
                {
                    'isBase64Encoded': False, 'statusCode': 200,
                    'body': '{"statusCode": 200, "message": "hello world", "user": {"name": "Lemi", "age": 1000000}}',
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'X-Content-Type-Options': 'nosniff'
                    }
                }
            )
            mock.patch.stopall()

    def test_scoped_middleware(self):
        class TestScopedMiddleware(Middleware):
            def __init__(self):
                super().__init__()
                self.scoped = True
                self.path_regex = re.compile(r"/hello/world")

        m = TestScopedMiddleware()
        self.assertTrue(m.scoped)
        # runs when path_regex matches request path
        self.assertTrue(m.run("/hello/world"))
        # does not run when path_regex does not match request path
        self.assertFalse(m.run("/hella/weird"))
