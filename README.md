[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checks](https://github.com/ProdPerfect/deez/actions/workflows/checks.yml/badge.svg)](https://github.com/ProdPerfect/deez/actions/workflows/checks.yml)
[![PyPI Release](https://github.com/ProdPerfect/deez/actions/workflows/release.yaml/badge.svg)](https://github.com/ProdPerfect/deez/actions/workflows/release.yaml)

# Deez

A little library to simplify building small APIs on top of AWS Lambda and API
Gateway.

> This library is still in development. It is sufficient for ProdPerfect's needs
> but it may not be for yours. Use at your own risk.

## Getting Started

### Requirements

- Python 3.9+
- Blinker 1.4+

### Installation

`pip install deez`

### Creating a resource

Your resource must implement at least one HTTP verb (get, post, put, etc.,)

```python
from deez.resource import Resource
from deez.response import JsonResponse


class MyResource(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world'})
```

### Example of how to use

`app.py`

````python
from deez import Deez
from deez.resource import Resource
from deez.response import JsonResponse
from deez.urls import path


class HelloWorldView(Resource):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world'})


app = Deez()
app.register_route(path("hello/world", HelloWorldView))

# or you can use regex
app.register_route(r'^hello/world$', HelloWorldView)


`middleware.py`

```python
from deez.middleware import Middleware


class User:
    # fake user object
    pass

class AuthMiddleware(Middleware):
    def before_request(self, request):
        # perhaps you want to authenticate the user and attach it to the request object
        request.user = User() 
        return request
````

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

### Signals

Deez supports signals. Signals are a way to hook into the request/response
lifecycle. This can be useful for logging metrics or doing other things such as
managing database connections.

```python
from deez.core.signals import request_finished, request_started


@request_started.connect
def my_callback(sender, **kwargs):
    print('request started')


@request_finished.connect
def my_other_callback(sender, **kwargs):
    print('request finished')
```

### Project Structure

See the `examples` directory for a working example.
