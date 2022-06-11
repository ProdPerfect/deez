import re
from typing import List

DEBUG = True
MIDDLEWARE: List[str] = []
CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
EXCEPTION_HANDLER = "deez.core.exception_handler.handler"

ACCESS_CONTROL_MAX_AGE: int = 86400
ACCESS_CONTROL_ALLOW_ORIGIN: str = '*'
