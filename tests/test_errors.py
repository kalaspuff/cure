import pytest

import cure
from cure import decorator


@pytest.mark.parametrize("value", [cure(), decorator(), cure.decorator()])
def test_missing_func(value):
    with pytest.raises(TypeError):
        value()


@pytest.mark.parametrize("value", [cure, decorator, cure.decorator])
def test_invalid_construct(value):
    new_value = value()
    with pytest.raises(TypeError):
        new_value()

    with pytest.raises(TypeError):
        new_value = value(4, 3, True, kw="yes")
    with pytest.raises(TypeError):
        new_value()
    with pytest.raises(TypeError):
        new_value(55)
    with pytest.raises(TypeError):
        new_value(lambda: None, extras=[])


@pytest.mark.parametrize("value", [cure(), decorator(), cure.decorator()])
def test_invalid_construct_no_meta(value):
    with pytest.raises(TypeError):
        value()
    with pytest.raises(TypeError):
        value(4, 3, True, kw="yes")
    with pytest.raises(TypeError):
        value(lambda: None, 3, True, kw="yes")


@pytest.mark.parametrize("value", [cure(), decorator(), cure.decorator()])
def test_invalid_argument(value):
    with pytest.raises(TypeError):
        value(1)

    with pytest.raises(TypeError):
        value("value")

    class X:
        def func(self, id_=0):
            return id_

    with pytest.raises(TypeError):
        value(X)

    x = X()
    with pytest.raises(TypeError):
        value(x)
