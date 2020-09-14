from deez.resource import Resource
from deez.response import HttpRedirectResponse, JsonResponse, NoContentResponse


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


class GetByNameResource(Resource):
    def get(self, request, customer_name):
        return JsonResponse(data={'message': 'ok', 'customer_name': customer_name}, headers={'X-Lemi-Gang': 'Yeet'})


class NotContentResource(HelloWorldResource):
    def get(self, request, *args, **kwargs):
        return NoContentResponse()


class RedirectResource(Resource):
    def get(self, request, *args, **kwargs):
        return HttpRedirectResponse('/redirect')
