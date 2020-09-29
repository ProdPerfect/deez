import re

DEBUG = True
MIDDLEWARE = ['deez.middleware.snakecase.SnakeCaseMiddleware']
CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
