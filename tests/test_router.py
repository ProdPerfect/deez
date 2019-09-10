import json
import os
import unittest
from deez import Deez
from deez.exceptions import NotFound404
from deez.resource import Resource
from deez.response import JsonResponse
from deez.router import Router
from tests.mock_event import event


class HelloWorldResource(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world'})


class HelloWorldSpecificResource(HelloWorldResource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world specific'})


class RouterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')
        app = Deez()
        self.router = Router(app)

    def test_can_route_correctly(self):
        self.router.register(r'^/hello/world$', HelloWorldResource)
        response = self.router.route(event, {})
        self.assertEqual(response, json.dumps({'message': 'hello world'}))

    def test_router_selects_most_specific_route(self):
        event['path'] = '/hello/world/1000/1000'
        self.router.register(r'^/hello/world/1000/1000', HelloWorldResource)
        self.router.register(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldSpecificResource)
        response = self.router.route(event, {})
        self.assertEqual(response, json.dumps({'message': 'hello world specific'}))

    def test_raises_404_when_route_not_found(self):
        self.router.register(r'^/hello/world/fail$', HelloWorldResource)
        with self.assertRaises(NotFound404) as e:
            self.router.route(event, {})
        self.assertEqual(e.exception.args[0], "GET '/hello/world' not found!")