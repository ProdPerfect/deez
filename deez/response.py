from typing import Dict
from deez.templates import TemplateLoader

try:
    from jinja2 import Template
    import ujson as json
except ImportError:
    from deez.templates import Template
    import json


class Response:
    TYPE = 'text/plain'

    def __init__(self, data=None):
        self.data = data

    def render(self, *args, **kwargs):
        return self.data


class JsonResponse(Response):
    TYPE = 'application/json'

    def render(self, *args, **kwargs):
        return json.dumps(self.data)


class HTMLResponse(Response):
    TYPE = 'text/html'

    def __init__(self, template_name: str = None, context: Dict = None, data=None) -> None:
        super().__init__(data=data)
        self._context = context
        self._template_name = template_name

    def render(self, loader: TemplateLoader) -> str:
        template = loader.get_template(self._template_name)
        return Template(template).render(**self._context)