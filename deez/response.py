try:
    import ujson as json
except ImportError:
    import json


class Response:
    TYPE = 'text/plain'

    def __init__(self, data=None, status_code=200):
        self.data = data
        self.status_code = status_code

    def render(self, *args, **kwargs):
        return self.data


class JsonResponse(Response):
    TYPE = 'application/json'

    def render(self, *args, **kwargs):
        return json.dumps(self.data)