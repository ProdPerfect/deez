from deez.middleware import Middleware


class User:
    def __init__(self):
        self.name = 'Lemi'
        self.age = 1_000_000

    def as_dict(self):
        return {'name': self.name, 'age': self.age}


class TestMiddleware(Middleware):
    def before_request(self, request):
        request.user = User()
        return request

    def before_response(self, response):
        data = response.data
        res = {'statusCode': 200, **data}
        response.data = res
        return response