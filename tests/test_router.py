import copy
import json
import os
import unittest

from deez import Deez
from deez.exceptions import NotFound404, ResourceError
from deez.resource import Resource
from deez.response import JsonResponse
from deez.router import Router
from tests.mock_event import event


class MethodNotImplementedResource(Resource):
    pass


class HelloWorldResource(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world'})


class HelloWorldResource2(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world 2'}, status_code=201)


class HelloWorldResource3(HelloWorldResource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world 3'})


class HelloWorldResource4(HelloWorldResource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world 3'}, headers={'X-Lemi-Gang': 'Yeet'})


class RouterTestCase(unittest.TestCase):

    def setUp(self, *args, **kwargs) -> None:
        os.environ.setdefault('PROJECT_SETTINGS_MODULE', 'settings')
        app = Deez()
        app.settings._reload()
        self.app = app
        self.router = Router(app)

    def test_can_route_correctly(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        router = Router(app)
        router.register(r'^/hello/world$', HelloWorldResource)
        response, status_code, _ = router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_respects_response_status_code(self, *args, **kwargs):
        app = Deez()
        app.settings._reload()
        router = Router(app)
        router.register(r'^/hello/world$', HelloWorldResource2)
        response, status_code, _ = router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world 2'}), response)
        self.assertEqual(status_code, 201)

    def test_router_selects_most_specific_route(self):
        event['path'] = '/hello/world/1000/1000'
        self.router.register(r'^/hello/world/1000/1000', HelloWorldResource)
        self.router.register(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldResource3)
        response, status_code, _ = self.router.execute(event, {})
        self.assertEqual(json.dumps({'message': 'hello world'}), response)
        self.assertEqual(status_code, 200)

    def test_user_provided_headers_are_returned_in_response(self):
        event['path'] = '/hello/world/1000/1000'
        self.router.register(r'^/hello/world/(?P<id>)\d{4}/(?P<pid>)\d{4}$', HelloWorldResource4)
        response = self.router.route(event, {})
        expected_headers = {'Access-Control-Allow-Origin': '*', 'X-Content-Type-Options': 'nosniff',
                            'Content-Type': 'application/json', 'X-Lemi-Gang': 'Yeet'}

        self.assertEqual(response['headers'], expected_headers)

    def test_resource_methods_not_implemented(self):
        _event = copy.deepcopy(event)
        _event['path'] = '/hello/world/1000/1000/1000'
        self.router.register(r'^/hello/world/1000/1000/1000', MethodNotImplementedResource)

        with self.assertRaises(ResourceError) as e:
            self.router.execute(_event, {})
        self.assertEqual(e.exception.args[0], "MethodNotImplementedResource's 'get' method not implemented!")

    def test_raises_404_when_route_not_found(self):
        self.router.register(r'^/hello/world/fail$', HelloWorldResource)
        with self.assertRaises(NotFound404) as e:
            self.router.execute(event, {})
        self.assertEqual("GET '/hello/world' not found!", e.exception.args[0])

    def test_raises_404_response(self):
        self.router.register(r'^/hello/world/fail$', HelloWorldResource)
        response = self.router.route(event, {})
        self.assertEqual({
            'isBase64Encoded': False,
            'statusCode': 404,
            'body': "GET '/hello/world' not found!",
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'X-Content-Type-Options': 'nosniff'
            }}, response)
