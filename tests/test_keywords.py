from convention import trail

import pytest


@pytest.mark.parametrize(
    "kw, expected",
    [
        ("a", "a"),
        ("as", "as_"),
        ("id", "id_"),
        ("id_", "id_"),
        ("uuid", "uuid"),
        ("uuid_", "uuid_"),
        ("str", "str_"),
        ("global", "global_"),
        ("key", "key"),
        ("pytest", "pytest"),
        ("syntax", "syntax"),
        ("del", "del_"),
        ("from", "from_"),
        ("globals", "globals_"),
        ("ord", "ord_"),
        ("pass", "pass_"),
        ("Exception", "Exception_"),
        ("exception", "exception"),
        ("exception_class", "exception_class"),
        ("password", "password"),
        ("user", "user"),
        ("__build_class__", "__build_class___"),
        ("dict", "dict_"),
        ("False", "False_"),
        ("ZeroDivisionError", "ZeroDivisionError_"),
    ],
)
def test_keyword(kw, expected):
    assert trail(kw) == expected
