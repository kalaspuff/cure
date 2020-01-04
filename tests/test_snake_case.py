import pytest

from cure import DEFAULT_OPTIONS, KEYWORD_SNAKE_CASE, KEYWORD_SNAKE_CASE_RECURSIVE, KEYWORD_TRAILING_UNDERSCORES, cure


def values(**kwargs):
    return kwargs


@pytest.mark.parametrize(
    "options, kwargs, expected",
    [
        (
            None,
            {
                "websiteAddress": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
            {
                "websiteAddress": "https://example.org/",
                "type_": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
        ),
        (
            DEFAULT_OPTIONS,
            {
                "websiteAddress": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
            {
                "websiteAddress": "https://example.org/",
                "type_": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
        ),
        (
            KEYWORD_SNAKE_CASE,
            {
                "websiteAddress": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
            {
                "website_address": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
        ),
        (
            KEYWORD_SNAKE_CASE_RECURSIVE,
            {
                "websiteAddress": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
            {
                "website_address": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "last_login": "2020-01-01T00:00:00.000000Z"},
            },
        ),
        (
            [KEYWORD_SNAKE_CASE_RECURSIVE, KEYWORD_TRAILING_UNDERSCORES],
            {
                "websiteAddress": "https://example.org/",
                "type": "subscription",
                "user": {"id": "4711", "lastLogin": "2020-01-01T00:00:00.000000Z"},
            },
            {
                "website_address": "https://example.org/",
                "type_": "subscription",
                "user": {"id": "4711", "last_login": "2020-01-01T00:00:00.000000Z"},
            },
        ),
        (
            KEYWORD_SNAKE_CASE_RECURSIVE,
            {"resources": [{"resourceId": "1", "data": "ABC"}, {"resourceId": "2", "data": "DEF"}]},
            {"resources": [{"resource_id": "1", "data": "ABC"}, {"resource_id": "2", "data": "DEF"}]},
        ),
    ],
)
def test_snake_case(options, kwargs, expected):
    if not options:
        decorator = cure()
    else:
        decorator = cure(options)
    assert decorator(values)(**kwargs) == expected
