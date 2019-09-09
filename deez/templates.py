"""
deez.templates
"""

__all__ = ['Template', 'TemplateLoader']

import glob
import os
from string import Template as BaseTemplate
from typing import Dict

from deez.exceptions import TemplateNotFound


class CustomTemplate(BaseTemplate):
    delimiter = "@@"


class Template:

    def __init__(self, template_string: str) -> None:
        """
        :param template_string: A string containing template variables
        """
        self.template_string = template_string
        self.rendered_template = ""

    def render(self, **kwargs) -> str:
        self.rendered_template = CustomTemplate(self.template_string).substitute(**kwargs)
        return self.rendered_template


class TemplateLoader:
    def __init__(self, settings):
        self.templates = {}
        self.template_dir = str(settings.TEMPLATE_DIR)

    @staticmethod
    def _read(_file):
        with open(_file, 'r') as f:
            return f.read()

    def _get_template_name(self, f):
        return f.replace(f'{self.template_dir}/', '')

    def get_template(self, template_name):
        template = self.templates.get(template_name)
        if template:
            return template
        raise TemplateNotFound(template_name)

    def find_templates(self) -> Dict[str, str]:
        templates = os.path.join(self.template_dir, '**/*.html')
        files = [f for f in glob.glob(templates, recursive=True)]
        for _, f in enumerate(files):
            template_name = self._get_template_name(f)
            self.templates[template_name] = self._read(f)
        return self.templates