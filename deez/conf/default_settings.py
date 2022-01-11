import re
from typing import List

DEBUG = True
MIDDLEWARE: List[str] = []
CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
EXCEPTION_HANDLER = "deez.core.exception_handler.handler"
