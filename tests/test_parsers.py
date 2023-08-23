import pytest

from deez.urls.parsers import alias_translator, register_alias


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("users/<int:name>/", r"^/users/(?P<name>\d+)/$"),
        ("users/<str:name>/", r"^/users/(?P<name>[a-zA-Z0-9-_]+)/$"),
        ("users/<slug:username>/", r"^/users/(?P<username>[-\w]+)/$"),
        ("users/<number:id>/", r"^/users/(?P<id>\d*[.,]?\d+)/$"),
        (
            "users/<uuid:name>/",
            r"^/users/(?P<name>[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/$",
        ),
    ],
)
def test_alias_translator(test_input, expected):
    assert alias_translator(test_input) == expected


def test_register_alias():
    register_alias("jira", r"DG-[0-3]{3}")

    url = alias_translator("tickets/<jira:id>/")
    assert url == r"^/tickets/(?P<id>DG-[0-3]{3})/$"
