from typing import Any, Dict
from app import get_application


# AWS Lambda entrypoint
def handler(event, context) -> Dict[str, Any]:
    app = get_application()
    return app.process_request(event, context)
