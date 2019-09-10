import json
import os
import unittest
from unittest import mock

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

    def setUp(self, *args, **kwargs) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')
        app = Deez()
        app.settings._reload()
        self.app = app
        self.router = Router(app)

    @mock.patch('tests.settings.MIDDLEWARE', return_value=[])
    def test_can_route_correctly(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        router = Router(app)
        router.register(r'^/hello/world$', HelloWorldResource)
        response = router.route(event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)

    def test_router_selects_most_specific_route(self):
        event['path'] = '/hello/world/1000/1000'
        self.router.register(r'^/hello/world/1000/1000', HelloWorldResource)
        self.router.register(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldSpecificResource)
        response = self.router.route(event, {})
        self.assertEqual(json.dumps({'message': 'hello world specific'}), response)

    def test_raises_404_when_route_not_found(self):
        self.router.register(r'^/hello/world/fail$', HelloWorldResource)
        with self.assertRaises(NotFound404) as e:
            self.router.route(event, {})
        self.assertEqual("GET '/hello/world' not found!", e.exception.args[0])