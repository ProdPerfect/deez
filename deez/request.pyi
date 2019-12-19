from typing import Any, Dict, Optional, Union


class Request:
    def __init__(self, event: Dict[str, Union], context: Any) -> None:
        self.path = None
        self.body = None
        self.headers: Optional[Dict[str, Union]] = None
        self.resource: Optional[str] = None
        self.identity: Optional[Dict[str, Union]] = None
        self.http_method: Optional[str] = None
        self.stage_variables: Optional[Dict[str, str]] = None
        self.path_parameters: Optional[Dict[str, str]] = None
        self.request_context: Optional[Dict[str, Union]] = None
        self.query_string_parameters: Optional[Optional[Dict[str, str]]] = None

        self.lambda_context: Any = context
        self._cleaned_event: Dict = event

    def _parse_event(self, event: Dict) -> Request:
        pass

    @staticmethod
    def _fixup_keys(key: str) -> str:
        pass
