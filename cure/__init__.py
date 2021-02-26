import builtins
import inspect
import keyword
import sys
import types
from enum import IntEnum
from functools import update_wrapper
from typing import Any, Callable, Dict, List, Tuple, Union, cast

from .builder import Builder
from .__version_data__ import __version__, __version_info__  # noqa

__author__ = "Carl Oscar Aaro"
__email__ = "hello@carloscar.com"

respected_keywords: set = set(dir(builtins)) | set(keyword.kwlist)


class Options(IntEnum):
    KEYWORD_TRAILING_UNDERSCORES = 1
    KEYWORD_SNAKE_CASE = 2
    KEYWORD_SNAKE_CASE_RECURSIVE = 4
    KEYWORD_CAMEL_CASE = 8
    KEYWORD_CAMEL_CASE_RECURSIVE = 16


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

    result = Builder.create_callable(
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

    return sorted(list(set(options)))


def is_keyword(kw: str) -> bool:
    return kw in respected_keywords


def trail_name(kw: str) -> str:
    if is_keyword(kw):
        return f"{kw}_"
    return kw


def snake_case_name(kw: str) -> str:
    result = ""

    for i, c in enumerate(kw.lower()):
        if i and c != kw[i]:
            result += "_"
        if c == "-":
            c = "_"

        result += c

    return result


def snake_case_dict(d: Dict, recursive: bool = True) -> Dict:
    result = {}

    for k, v in d.items():
        if recursive and isinstance(v, Dict):
            v = snake_case_dict(v, recursive)
        if recursive and isinstance(v, List):
            v = [snake_case_dict(x, recursive) for x in v]

        result[snake_case_name(k)] = v

    return result


def camel_case_name(kw: str) -> str:
    result = ""

    next_upper = False
    for i, c in enumerate(kw):
        if c in ("-", "_"):
            next_upper = True
            continue
        if next_upper:
            result += c.upper()
            next_upper = False
        else:
            result += c

    return result


def camel_case_dict(d: Dict, recursive: bool = True) -> Dict:
    result = {}

    for k, v in d.items():
        if recursive and isinstance(v, Dict):
            v = camel_case_dict(v, recursive)
        if recursive and isinstance(v, List):
            v = [camel_case_dict(x, recursive) for x in v]

        result[camel_case_name(k)] = v

    return result


def _cure(func: Callable, options: List, *args: Any, **kwargs: Any) -> Any:
    new_kwargs = kwargs

    if Options.KEYWORD_CAMEL_CASE_RECURSIVE in options:
        new_kwargs = camel_case_dict(new_kwargs, recursive=True)
    elif Options.KEYWORD_CAMEL_CASE in options:
        new_kwargs = camel_case_dict(new_kwargs, recursive=False)

    if Options.KEYWORD_SNAKE_CASE_RECURSIVE in options:
        new_kwargs = snake_case_dict(new_kwargs, recursive=True)
    elif Options.KEYWORD_SNAKE_CASE in options:
        new_kwargs = snake_case_dict(new_kwargs, recursive=False)

    if Options.KEYWORD_TRAILING_UNDERSCORES in options:
        new_kwargs = {trail_name(k): v for k, v in new_kwargs.items()}

    return func(*args, **new_kwargs)


def cure_decorator(*pargs: Any, **pkwargs: Any) -> Callable:
    options = get_options(*pargs, **pkwargs)

    def caller(*args: Any, **kwargs: Any) -> Any:
        func, *args = args  # type: ignore
        return _cure(func, options, *args, **kwargs)

    decorator = Builder.create_callable(
        "_decorator_wrapper_(*f)",
        "return _decorate_(None, _call_) if not f else _decorate_(f[0], _call_)",
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
    __version_info__: Tuple[Union[int, str], ...] = __version_info__  # noqa
    __author__: str = __author__
    __email__: str = __email__

    Options = Options
    options = Options
    DEFAULT_OPTIONS = DEFAULT_OPTIONS

    KEYWORD_TRAILING_UNDERSCORES = Options.KEYWORD_TRAILING_UNDERSCORES
    KEYWORD_SNAKE_CASE = Options.KEYWORD_SNAKE_CASE
    KEYWORD_SNAKE_CASE_RECURSIVE = Options.KEYWORD_SNAKE_CASE_RECURSIVE
    KEYWORD_CAMEL_CASE = Options.KEYWORD_CAMEL_CASE
    KEYWORD_CAMEL_CASE_RECURSIVE = Options.KEYWORD_CAMEL_CASE_RECURSIVE

    def __init__(self) -> None:
        self.decorator = CureDecorator(cure_decorator)
        self.cure = self.decorator

        self.get_options = get_options

        self.respected_keywords = respected_keywords
        self.is_keyword = is_keyword
        self.trail_name = trail_name

        self.snake_case_name = snake_case_name
        self.snake_case_dict = snake_case_dict

        self.camel_case_name = camel_case_name
        self.camel_case_dict = camel_case_dict

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
KEYWORD_SNAKE_CASE = Options.KEYWORD_SNAKE_CASE
KEYWORD_SNAKE_CASE_RECURSIVE = Options.KEYWORD_SNAKE_CASE_RECURSIVE
KEYWORD_CAMEL_CASE = Options.KEYWORD_CAMEL_CASE
KEYWORD_CAMEL_CASE_RECURSIVE = Options.KEYWORD_CAMEL_CASE_RECURSIVE

_actual_module = sys.modules[__name__]  # noqa

cure_instance.__spec__ = _actual_module.__spec__  # type: ignore
cure_instance.__path__ = _actual_module.__path__  # type: ignore
cure_instance.__cached__ = _actual_module.__cached__  # type: ignore
cure_instance.__dict__ = _actual_module.__dict__
cure_instance.__doc__ = _actual_module.__doc__
cure_instance.__file__ = _actual_module.__file__  # type: ignore
cure_instance.__name__ = _actual_module.__name__  # type: ignore
cure_instance.__package__ = _actual_module.__package__  # type: ignore

sys.modules[__name__] = cure_instance  # type: ignore
