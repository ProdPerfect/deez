import json
from typing import Dict
from deez.templates import TemplateLoader

try:
    from jinja2 import Template
except ImportError:
    from deez.templates import Template


class Response:
    TYPE = 'text'

    def __init__(self, data=None):
        self._data = data

    def render(self, *args, **kwargs):
        return self._data


class JsonResponse(Response):
    TYPE = 'json'

    def render(self, *args, **kwargs):
        return json.dumps(self._data)


class HTMLResponse(Response):
    TYPE = 'html'

    def __init__(self, template_name: str = None, context: Dict = None, data=None) -> None:
        super().__init__(data=data)
        self._context = context
        self._template_name = template_name

    def render(self, loader: TemplateLoader) -> str:
        template = loader.get_template(self._template_name)
        return Template(template).render(**self._context)