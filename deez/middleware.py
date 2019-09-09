class Middleware:
    def __init__(self, resource):
        self.resource = resource

    def before_request(self, request):
        pass

    def before_response(self, response):
        pass