import pytest

import convention
from convention import decorator


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_wrapper(value):
    func = value(lambda x: x)
    assert func("input_data") == "input_data"


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_wrapped_class_func(value):
    class X:
        def func(self, id_=0):
            return id_

    assert value(X().func)(4711) == 4711
    assert value(X().func)() == 0
    assert value(X().func)(id=1337) == 1337
    assert value(X().func)(id_=1338) == 1338
    assert value(X().func)(**{"id": -5050}) == -5050
    assert value(X().func)(**{"id_": 999999}) == 999999


@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_decorated_class_func(value):
    class X:
        @value
        def func(self, id_=0):
            return id_

        def non_decorated_func(self, id_=0):
            return id_

    assert X().func(4711) == 4711
    assert X().func() == 0
    assert X().func(id=1337) == 1337
    assert X().func(id_=1338) == 1338
    assert X().func(**{"id": -5050}) == -5050
    assert X().func(**{"id_": 999999}) == 999999

    x = X()
    assert x.func(4711) == 4711
    assert x.func() == 0
    assert x.func(id=1337) == 1337
    assert x.func(id_=1338) == 1338
    assert x.func(**{"id": -5050}) == -5050
    assert x.func(**{"id_": 999999}) == 999999

    assert x.non_decorated_func(**{"id_": 999999}) == 999999
    with pytest.raises(TypeError):
        assert x.non_decorated_func(**{"id": 999999}) == 999999

@pytest.mark.parametrize("value", [convention, decorator, convention.decorator, convention(), decorator(), convention.decorator()])
def test_failed_kwargs(value):
    func = lambda id=None: "42"
    assert func(None) == "42"
    assert func(id=1338) == "42"
    with pytest.raises(TypeError):
        assert func(id_=1338) == "42"
    assert func(**{"id": 4711}) == "42"
    with pytest.raises(TypeError):
        assert func(**{"id_": 4711}) == "42"

    func = lambda id_=None: "42"
    assert func(None) == "42"
    with pytest.raises(TypeError):
        assert func(id=1338) == "42"
    assert func(id_=1338) == "42"
    with pytest.raises(TypeError):
        assert func(**{"id": 4711}) == "42"
    assert func(**{"id_": 4711}) == "42"

    func = value(lambda id=None: "42")
    assert func(None) == "42"
    with pytest.raises(TypeError):
        assert func(id=1338) == "42"
    with pytest.raises(TypeError):
        assert func(id_=1338) == "42"
    with pytest.raises(TypeError):
        assert func(**{"id": 4711}) == "42"
    with pytest.raises(TypeError):
        assert func(**{"id_": 4711}) == "42"

    func = value(lambda id_=None: "42")
    assert func(None) == "42"
    assert func(id=1338) == "42"
    assert func(id_=1338) == "42"
    assert func(**{"id": 4711}) == "42"
    assert func(**{"id_": 4711}) == "42"
