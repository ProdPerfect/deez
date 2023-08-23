from deez.resource import Resource
from deez.response import JsonResponse
from deez.request import Request


class IndexResource(Resource):
    def get(self, request: Request, *args, **kwargs) -> JsonResponse:
        print(request.params)  # contains the query string parameters
        return JsonResponse({"message": "Hello, World!"})

    def post(self, request: Request, *args, **kwargs) -> JsonResponse:
        print(request.data)  # contains the request body
        return JsonResponse({"message": "Hello, World!"})
