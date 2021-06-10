import copy
import json
import os
import unittest

from deez.deez import Deez
from deez.exceptions import MethodNotAllowed, NotFound
from deez.urls import path
from tests.mock_event import event
from tests.mock_resources import (
    GetByNameResource, HelloWorldResource, HelloWorldResource2,
    HelloWorldResource3, HelloWorldResource4, MethodNotImplementedResource,
    NotContentResource, RedirectResource,
)


class RouterTestCase(unittest.TestCase):

    def setUp(self, *args, **kwargs) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')
        app = Deez()
        app.settings._reload()
        self.app = app
        self.router = app.router

    def test_can_route_correctly(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        app.register_route(r'^/hello/world$', HelloWorldResource)
        response, status_code, _, _ = app.router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_can_route_correctly_with_str_path(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        app.register_route(path('/hello/<str:customer_name>', GetByNameResource))
        response, status_code, _, _ = app.router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'ok', 'customer_name': 'world'}), response)
        self.assertEqual(status_code, 200)

        _event = copy.deepcopy(event)
        _event['path'] = '/hello/my-world'
        response, status_code, _, _ = app.router.execute(_event, {})
        self.assertEqual(json.dumps({'message': 'ok', 'customer_name': 'my-world'}), response)
        self.assertEqual(status_code, 200)

    def test_can_route_correctly_with_int_path(self, *args, **kwargs):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/1/'
        app = Deez()
        app.settings._reload()
        app.register_route(path('/hello/<int:world>/', HelloWorldResource))
        response, status_code, _, _ = app.router.execute(_event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_can_route_correctly_with_number_path(self, *args, **kwargs):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/10.00/stacks'
        app = Deez()
        app.settings._reload()
        app.register_route(path('/hello/<number:world>/stacks', HelloWorldResource))
        response, status_code, _, _ = app.router.execute(_event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_can_route_correctly_with_uuid_path(self, *args, **kwargs):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/b4464968-98a3-4019-b198-83155241a8a6'
        app = Deez()
        app.settings._reload()
        app.register_route(path('/hello/<uuid:world>', HelloWorldResource))
        response, status_code, _, _ = app.router.execute(_event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_can_route_correctly_with_slug_path(self, *args, **kwargs):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/hello-world-hello'
        app = Deez()
        app.settings._reload()
        app.register_route(path('/hello/<slug:world>', HelloWorldResource))
        response, status_code, _, _ = app.router.execute(_event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_respects_response_status_code(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        app.register_route(r'^/hello/world$', HelloWorldResource2)
        response, status_code, _, _ = app.router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world 2'}), response)
        self.assertEqual(status_code, 201)

    def test_router_selects_most_specific_route(self):
        event['path'] = '/hello/world/1000/1000'
        self.app.register_route(r'^/hello/world/1000/1000', HelloWorldResource)
        self.app.register_route(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldResource3)
        response, status_code, _, _ = self.router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_user_provided_headers_are_returned_in_response(self):
        event['path'] = '/hello/world/1000/1000'
        self.app.register_route(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldResource4)
        response = self.router.route(event, {})
        expected_headers = {'Access-Control-Allow-Origin': '*', 'X-Content-Type-Options': 'nosniff',
                            'Content-Type': 'application/json', 'X-Lemi-Gang': 'Yeet'}

        self.assertEqual(response['headers'], expected_headers)

    def test_no_content_response(self):
        _event = copy.deepcopy(event)
        _event['path'] = '/no-content'
        self.app.register_route(r'^/no-content$', NotContentResource)
        response = self.router.route(_event, {})
        expected_headers = {'Access-Control-Allow-Origin': '*', 'X-Content-Type-Options': 'nosniff'}
        self.assertEqual(expected_headers, response['headers'])

    def test_resource_methods_not_implemented(self):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/world/1000/1000/1000'
        self.app.register_route(r'^/hello/world/1000/1000/1000', MethodNotImplementedResource)

        with self.assertRaises(MethodNotAllowed) as e:
            self.router.execute(_event, {})
        self.assertEqual(e.exception.args[0], 'method not allowed!')

    def test_raises_404_when_route_not_found(self):
        self.app.register_route(r'^/hello/world/fail$', HelloWorldResource)
        with self.assertRaises(NotFound) as e:
            self.router.execute(event, {})
        self.assertEqual("GET '/hello/world' not found!", e.exception.args[0])

    def test_redirect_response(self):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/world/redirect'

        self.app.register_route(path('hello/world/redirect', RedirectResource))
        response = self.router.route(_event, {})

        self.assertEqual({
            'isBase64Encoded': False,
            'statusCode': 302,
            'body': None,
            'headers': {
                'Location': '/redirect',
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'X-Content-Type-Options': 'nosniff'
            }}, response)

    def test_raises_404_response(self):
        self.app.register_route(r'^/hello/world/fail$', HelloWorldResource)
        response = self.router.route(event, {})
        self.assertEqual({
            'isBase64Encoded': False,
            'statusCode': 404,
            'body': '{"message": "GET \'/hello/world\' not found!"}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'X-Content-Type-Options': 'nosniff'
            }}, response)
