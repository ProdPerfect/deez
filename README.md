# Deez
A little library to simplify building small APIs on top of AWS Lambda + API Gateway.

> ##### DOCUMENTATION TBD

### Installation
`pip install deez`


### Creating a resource
Your resource must implement an HTTP verb (get, post, put, etc.,)

```python
from deez.resource import Resource

class MyResource(Resource):
    def get(self, request, *args, **kwargs):
        pass
```

### Example of how to use
Note: The Deez router uses regex for path matching.

`app.py`
```python
from deez import Deez
from deez.resource import Resource
from deez.response import JsonResponse


class HelloWorldView(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world'})


app = Deez()
app.register_route('^hello/world$', HelloWorldView)
```

`middleware.py`
```python
from deez.middleware import Middleware

class User:
    # fake user object
    pass

class AuthMiddleware(Middleware):
    def before_request(self, request):
        # do auth things
        request.user = User() 
        return request
```

`settings.py`
```python
# middleware runs before views are called and before the response is returned
# so you can manipulate the response and requests objects.
MIDDLEWARE = ['middleware.AuthMiddleware']
```

`handler.py`
```python

from app import app

def handle_event(event, context):
    return app.process_request(event, context)
```
