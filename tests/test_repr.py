import convention
from convention import decorator


def test_repr():
    id_ = hex(id(convention))
    assert str(convention) == f"<convention.decorator object at {id_}>"
    assert str(convention.decorator) != f"<convention.decorator object at {id_}>"
    assert str(decorator) == str(convention.decorator)

    assert repr(convention) == f"<convention.decorator object at {id_}>"
    assert repr(convention.decorator) != f"<convention.decorator object at {id_}>"
    assert repr(decorator) == repr(convention.decorator)

    assert convention is not convention.decorator
    assert convention is not decorator
    assert convention.decorator is decorator

    assert str(convention()) != f"<convention.decorator object at {id_}>"
    assert str(convention.decorator()) != f"<convention.decorator object at {id_}>"
    assert str(decorator()) != f"<convention.decorator object at {id_}>"

    assert repr(convention()) != f"<convention.decorator object at {id_}>"
    assert repr(convention.decorator()) != f"<convention.decorator object at {id_}>"
    assert repr(decorator()) != f"<convention.decorator object at {id_}>"

    assert str(convention()).startswith("<convention.decorator object at")
    assert str(convention.decorator()).startswith("<convention.decorator object at")
    assert str(decorator()).startswith("<convention.decorator object at")

    assert repr(convention()).startswith("<convention.decorator object at")
    assert repr(convention.decorator()).startswith("<convention.decorator object at")
    assert repr(decorator()).startswith("<convention.decorator object at")

    assert str(convention()) != str(convention)
    assert str(convention()) != str(convention())
    assert str(convention()) != str(convention.decorator())
    assert str(convention()) != str(decorator())


def test_wrapped_repr():
    id_ = hex(id(convention))
    assert str(convention) == f"<convention.decorator object at {id_}>"
    assert str(convention.decorator) != f"<convention.decorator object at {id_}>"
    assert str(decorator) == str(convention.decorator)

    def wrapped_func():
        pass

    func_id = hex(id(wrapped_func))
    func = convention(wrapped_func)

    start_str = "function test_wrapped_repr.<locals>.wrapped_func at"

    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) == f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) == f"<{start_str} {func_id}>"

    func = convention(4711, 1338, a=1, b=2, **{"id": 55})(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) == f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) == f"<{start_str} {func_id}>"

    func = convention.decorator(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) == f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) == f"<{start_str} {func_id}>"

    func = convention.decorator()(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) == f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) == f"<{start_str} {func_id}>"
