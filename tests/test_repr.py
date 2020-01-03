import cure
from cure import decorator


def test_repr():
    id_ = hex(id(cure))
    assert str(cure) == f"<cure.decorator at {id_}>"
    assert str(cure.decorator) != f"<cure.decorator at {id_}>"
    assert str(decorator) == str(cure.decorator)

    assert repr(cure) == f"<cure.decorator at {id_}>"
    assert repr(cure.decorator) != f"<cure.decorator at {id_}>"
    assert repr(decorator) == repr(cure.decorator)

    assert cure is not cure.decorator
    assert cure is not decorator
    assert cure.decorator is decorator

    assert str(cure()) != f"<cure.decorator at {id_}>"
    assert str(cure.decorator()) != f"<cure.decorator at {id_}>"
    assert str(decorator()) != f"<cure.decorator at {id_}>"

    assert repr(cure()) != f"<cure.decorator at {id_}>"
    assert repr(cure.decorator()) != f"<cure.decorator at {id_}>"
    assert repr(decorator()) != f"<cure.decorator at {id_}>"

    assert str(cure()).startswith("<cure.decorator at")
    assert str(cure.decorator()).startswith("<cure.decorator at")
    assert str(decorator()).startswith("<cure.decorator at")

    assert repr(cure()).startswith("<cure.decorator at")
    assert repr(cure.decorator()).startswith("<cure.decorator at")
    assert repr(decorator()).startswith("<cure.decorator at")

    assert str(cure()) != str(cure)
    assert str(cure()) != str(cure())
    assert str(cure()) != str(cure.decorator())
    assert str(cure()) != str(decorator())


def test_wrapped_repr():
    id_ = hex(id(cure))
    assert str(cure) == f"<cure.decorator at {id_}>"
    assert str(cure.decorator) != f"<cure.decorator at {id_}>"
    assert str(decorator) == str(cure.decorator)

    def wrapped_func():
        pass

    func_id = hex(id(wrapped_func))
    func = cure(wrapped_func)

    start_str = "function test_wrapped_repr.<locals>.wrapped_func at"

    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) != f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) != f"<{start_str} {func_id}>"

    func = cure()(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) != f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) != f"<{start_str} {func_id}>"

    func = cure.decorator(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) != f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) != f"<{start_str} {func_id}>"

    func = cure.decorator()(wrapped_func)
    assert str(func) != f"<{start_str} {id_}>"
    assert str(func) != f"<{start_str} {func_id}>"
    assert repr(func) != f"<{start_str} {id_}>"
    assert repr(func) != f"<{start_str} {func_id}>"
