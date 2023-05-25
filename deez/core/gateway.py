from typing import Any, Dict, Union


def api_gateway_response(
    status_code: int,
    data: Any,
    content_type: str = "application/json",
    extra_headers: Union[Dict[str, str], None] = None,
) -> Dict[str, Any]:
    """
    Response formatted in a way that API Gateway
    can understand.
    """
    default_headers = {
        "Access-Control-Allow-Origin": "*",
        "X-Content-Type-Options": "nosniff",
    }

    if content_type:
        default_headers["Content-Type"] = content_type

    if extra_headers:
        default_headers.update(**extra_headers)

    response = {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "body": data,
        "headers": default_headers,
    }
    return response
