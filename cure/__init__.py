import builtins
import inspect
import keyword
import sys
import types
from enum import IntEnum
from functools import update_wrapper
from typing import Any, Callable, List, Tuple, cast

from decorator import FunctionMaker

from .__version__ import __version__, __version_info__  # noqa

__author__ = "Carl Oscar Aaro"
__email__ = "hello@carloscar.com"

respected_keywords: set = set(dir(builtins)) | set(keyword.kwlist)


class Options(IntEnum):
    KEYWORD_TRAILING_UNDERSCORES = 1


options = Options

DEFAULT_OPTIONS = [Options.KEYWORD_TRAILING_UNDERSCORES]


def decorate(func: Callable, caller: Callable) -> Callable:
    if not func:
        raise TypeError("'cure.decorator' must decorate a callable")

    bound_arg = None
    is_staticmethod = False
    is_classmethod = False
    if not isinstance(func, types.FunctionType) and isinstance(func, staticmethod):
        func = func.__func__
        is_staticmethod = True
    elif not isinstance(func, types.FunctionType) and isinstance(func, classmethod):
        func = func.__func__
        is_classmethod = True
    elif (
        not isinstance(func, types.FunctionType)
        and getattr(func, "__func__", None)
        and getattr(func, "__self__", None)
        and inspect.ismethod(func)
    ):
        bound_arg = getattr(func, "__self__")
        func = func.__func__  # type: ignore

    if (
        not callable(func)
        and not isinstance(func, (staticmethod, classmethod))
        and not isinstance(func, types.FunctionType)
    ):
        raise TypeError("'cure.decorator' must decorate a callable")

    if not inspect.isfunction(func) and not inspect.ismethod(func):
        raise TypeError("'cure.decorator' can only decorate a function")

    name = "_decorated_function_"
    if inspect.isfunction(func):
        name = func.__name__ if not func.__name__ == "<lambda>" else "_lambda_"

    signature = f"{name}(*args, **kwargs)"

    result = FunctionMaker.create(
        signature, "return _call_(_func_, *args, **kwargs)", {"_call_": caller, "_func_": func}, __wrapped__=func
    )

    if hasattr(func, "__qualname__"):
        result.__qualname__ = func.__qualname__

    if bound_arg:
        result = result.__get__(bound_arg)  # type: ignore
    if is_staticmethod:
        result = staticmethod(result)  # type: ignore
    if is_classmethod:
        result = classmethod(result)  # type: ignore

    return result


def get_options(*args: Any, **kwargs: Any) -> List:
    if (
        args
        and not kwargs
        and len(args) == 1
        and (
            callable(args[0])
            or (isinstance(args[0], (staticmethod, classmethod)) and not isinstance(args[0], types.FunctionType))
        )
    ):
        return DEFAULT_OPTIONS

    if not args and not kwargs:
        return DEFAULT_OPTIONS

    if len(args) > 1:
        args = tuple([args])

    if args and not isinstance(args[0], (tuple, list, int)):
        raise TypeError("Invalid options")

    if args and args[0] == DEFAULT_OPTIONS:
        return DEFAULT_OPTIONS

    options = []
    if args:
        if isinstance(args[0], (tuple, list)):
            values = list(map(lambda x: str(x).upper(), [x for x in args[0] if x]))
            for o in Options:
                if str(o.value) in values or str(o).upper() in values or str(o).upper().split(".")[1] in values:
                    options.append(o)
                    values = list(
                        filter(
                            lambda x: x != str(o.value) and x != str(o).upper() and x != str(o).upper().split(".")[1],
                            values,
                        )
                    )
            if values:
                raise TypeError("Invalid options: unknown values '" + "', '".join(values) + "'")
        elif isinstance(args[0], int):
            total = 0
            for o in Options:
                total += o.value
                if o.value & args[0] == o.value:
                    options.append(o)
            if args[0] & total != args[0]:
                raise TypeError("Invalid options: unknown option supplied")

    if kwargs:
        values = [str(k).upper() for k, v in kwargs.items() if v]
        for o in Options:
            if str(o).upper().split(".")[1] in values:
                options.append(o)
                values.remove(str(o).upper().split(".")[1])
        if values:
            raise TypeError("Invalid options: unknown values '" + "', '".join(values) + "'")

    if not options:
        raise TypeError("Invalid options: No options chosen")

    return list(set(options))


def is_keyword(kw: str) -> bool:
    return kw in respected_keywords


def trail_name(kw: str) -> str:
    if is_keyword(kw):
        return f"{kw}_"
    return kw


def _cure(func: Callable, options: List, *args: Any, **kwargs: Any) -> Any:
    new_kwargs = kwargs

    if Options.KEYWORD_TRAILING_UNDERSCORES in options:
        new_kwargs = {trail_name(k): v for k, v in new_kwargs.items()}

    return func(*args, **new_kwargs)


def cure_decorator(*pargs: Any, **pkwargs: Any) -> Callable:
    options = get_options(*pargs, **pkwargs)

    def caller(*args: Any, **kwargs: Any) -> Any:
        func, *args = args  # type: ignore
        return _cure(func, options, *args, **kwargs)

    decorator = FunctionMaker.create(
        "_decorator_wrapper_(*f)",
        "if not f: return _decorate_(None, _call_)\n" "return _decorate_(f[0], _call_)",
        {"_call_": caller, "_decorate_": decorate},
        module=caller.__module__,
        __wrapped__=caller,
    )

    if (
        pargs
        and not pkwargs
        and len(pargs) == 1
        and (
            callable(pargs[0])
            or (isinstance(pargs[0], (staticmethod, classmethod)) and not isinstance(pargs[0], types.FunctionType))
        )
    ):
        result = decorator(pargs[0])
    else:
        result = decorator

    return cast(Callable, result)


class CureDecorator(object):
    def __init__(self, func: Callable) -> None:
        self.func = func
        update_wrapper(self, func)

    def __call__(self, *args: Any, **kwargs: Any) -> Callable:
        result = self.func(*args, **kwargs)
        if getattr(result, "__qualname__", None) == "_decorator_wrapper_":
            return CureDecorator(result)
        return cast(Callable, result)

    def __repr__(self) -> str:
        id_ = hex(id(self))
        return f"<cure.decorator at {id_}>"


class Cure(object):
    __version__: str = __version__  # noqa
    __version_info__: Tuple[int, int, int] = __version_info__  # noqa
    __author__: str = __author__
    __email__: str = __email__

    Options = Options
    options = Options
    DEFAULT_OPTIONS = DEFAULT_OPTIONS

    KEYWORD_TRAILING_UNDERSCORES = Options.KEYWORD_TRAILING_UNDERSCORES

    def __init__(self) -> None:
        self.decorator = CureDecorator(cure_decorator)
        self.cure = self.decorator

        self.respected_keywords = respected_keywords
        self.is_keyword = is_keyword
        self.trail_name = trail_name
        self.get_options = get_options

        update_wrapper(self, cure_decorator)

    def __call__(self, *args: Any, **kwargs: Any) -> Callable:
        result = cure_decorator(*args, **kwargs)
        if getattr(result, "__qualname__", None) == "_decorator_wrapper_":
            return CureDecorator(result)
        return result

    def __repr__(self) -> str:
        id_ = hex(id(self))
        return f"<cure.decorator at {id_}>"


cure_instance = Cure()

decorator = cure_instance.decorator
cure = cure_instance.decorator

KEYWORD_TRAILING_UNDERSCORES = Options.KEYWORD_TRAILING_UNDERSCORES

sys.modules[__name__] = cure_instance  # type: ignore
