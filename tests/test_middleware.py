import json
import os
import unittest
from unittest import mock

from deez import Deez
from deez.resource import Resource
from deez.response import JsonResponse
from deez.router import Router
from tests.mock_event import event


class HelloWorldResource(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world', 'user': request.user.as_dict()})


class MiddlewareTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'tests.settings')

    @mock.patch('tests.settings.MIDDLEWARE', ['tests.middleware.TestMiddleware'])
    def test_can_route_correctly(self):
        app = Deez()
        router = Router(app)
        router.register(r'^/hello/world$', HelloWorldResource)
        response = router.route(event, {})
        self.assertEqual(response, json.dumps(
            {
                'statusCode': 200,
                'message': 'hello world',
                'user': {
                    'name': 'Lemi',
                    'age': 1000000
                }
            }))