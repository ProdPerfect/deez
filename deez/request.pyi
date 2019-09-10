from typing import Any, Dict, NoReturn, Optional, Union


class Request:
    def __init__(self, event: Dict[str, Union], context: Any) -> NoReturn:
        self.path = None
        self.body = None
        self.headers: Dict[str, Union] = None
        self.resource: str = None
        self.identity: Dict[str, Union] = None
        self.http_method: str = None
        self.stage_variables: Dict[str, str] = None
        self.path_parameters: Dict[str, str] = None
        self.request_context: Dict[str, Union] = None
        self.query_string_parameters: Optional[Dict[str, str]] = None

        self.lambda_context: Any = context
        self._cleaned_event: Dict = event

    def _parse_event(self, event: Dict) -> Request:
        pass

    @staticmethod
    def _fixup_keys(key: str) -> str:
        pass