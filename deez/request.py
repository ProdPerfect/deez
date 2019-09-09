class Request:
    def __init__(self, path, method, headers=None, event=None, context=None, body=None, url_params=None):
        self.path = path
        self.event = event
        self.method = method
        self.headers = headers
        self.context = context
        self.body = body if body else {}
        self.url_params = url_params if url_params else {}