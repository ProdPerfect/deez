class Middleware:
    def __init__(self, view):
        self.view = view

    def before_request(self, request):
        pass

    def before_response(self, response):
        pass