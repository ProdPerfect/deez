import json
from deez.request import Request


def test_request_params() -> None:
    request = Request(
        {
            "httpMethod": "GET",
            "path": "/",
            "queryStringParameters": {"foo": "bar"},
        },
        {},
    )
    assert request.params["foo"] == "bar"


def test_request_data() -> None:
    request = Request(
        {
            "httpMethod": "POST",
            "path": "/",
            "body": json.dumps({"foo": "bar"}),
        },
        {},
    )
    assert request.data["foo"] == "bar"


def test_request_data_invalid_json() -> None:
    request = Request(
        {
            "httpMethod": "POST",
            "path": "/",
            "body": "hello world",
        },
        {},
    )
    assert request.data == {}
