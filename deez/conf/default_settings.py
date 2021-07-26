import re

DEBUG = True
MIDDLEWARE = []
CAMELCASE_REGEX = re.compile(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])')
EXCEPTION_HANDLER = "deez.core.exception_handler.handler"
LOGGER_MESSAGE_FORMAT = "%(asctime)s %(levelname)s %(message)s"
