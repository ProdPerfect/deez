class Middleware:
    def before_request(self, request):
        return request

    def before_response(self, response):
        return response
