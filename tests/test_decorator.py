import pytest

import convention
from convention import decorator


def test_func_without_decorator():
    def func(context, url=None, method=None, query=None, global_=None, id_=None, syntax_=None, credentials=None):
        return (url, method, id_, [global_, syntax_], credentials is None)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global_": "yes",
        "syntax_": 4711,
        "id_": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    assert func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_func_with_decorator(value):
    @value
    def func(context, url=None, method=None, query=None, global_=None, id_=None, syntax_=None, credentials=None):
        return (url, method, id_, [global_, syntax_], credentials is None)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global": "yes",
        "syntax_": 4711,
        "id": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    assert func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_func_with_decorator_pre_trailed(value):
    @value
    def func(context, url=None, method=None, query=None, global_=None, id_=None, syntax_=None, credentials=None):
        return (url, method, id_, [global_, syntax_], credentials is None)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global_": "yes",
        "syntax_": 4711,
        "id_": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    assert func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_func_with_kwargs(value):
    @value
    def func(context, **input_kwargs):
        assert len(input_kwargs) == 5
        return (input_kwargs["url"], input_kwargs["method"], input_kwargs["id_"], [input_kwargs["global_"], input_kwargs["syntax_"]], "credentials" not in input_kwargs)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global": "yes",
        "syntax_": 4711,
        "id": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    assert func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_wrapped_func(value):
    def func(context, url=None, method=None, query=None, global_=None, id_=None, syntax_=None, credentials=None):
        return (url, method, id_, [global_, syntax_], credentials is None)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global": "yes",
        "syntax_": 4711,
        "id": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    wrapped_func = value(func)

    assert wrapped_func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_wrapped_and_decorated_func(value):
    @value
    def func(context, url=None, method=None, query=None, global_=None, id_=None, syntax_=None, credentials=None):
        return (url, method, id_, [global_, syntax_], credentials is None)

    context = {}
    kwargs = {
        "url": "http://example.org/",
        "method": "GET",
        "global": "yes",
        "syntax_": 4711,
        "id": "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3"
    }

    wrapped_func = value(func)

    assert wrapped_func(context, **kwargs) == ("http://example.org/", "GET", "7e8f65c7-24e3-4739-b7f2-1286d0d36fa3", ["yes", 4711], True)
