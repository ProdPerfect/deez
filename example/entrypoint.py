from typing import Any, Dict

from app import get_application


# AWS Lambda entrypoint
def handler(event, context) -> Dict[str, Any]:
    # note: if your app receives a lot of traffic,
    # you should consider instantiating the app outside of the handler.
    app = get_application()
    return app.process_request(event, context)
