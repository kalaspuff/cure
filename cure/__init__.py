import builtins
from functools import update_wrapper
import keyword
import types
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple, Type, Union, cast  # noqa
import sys

from .__version__ import __version__, __version_info__  # noqa

__author__ = "Carl Oscar Aaro"
__email__ = "hello@carloscar.com"


class DecoratorMetaClass(type):
    def __new__(cls, name: str, bases: Tuple[type, ...], attributedict: Dict) -> "DecoratorMetaClass":
        result: Type[DecoratorBaseClass] = type.__new__(cls, name, bases, attributedict)
        return result


class DecoratorBaseClass(metaclass=DecoratorMetaClass):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if not isinstance(self, cure):
            self._meta = False

        try:
            if self._args_is_decorated_function(*args, **kwargs):
                func: Any = args[0]

                self._staticmethod = isinstance(func, staticmethod)
                self._classmethod = isinstance(func, classmethod)
                if not isinstance(func, types.FunctionType) and (self._staticmethod or self._classmethod):
                    func = func.__func__

                self.__closure__ = func.__closure__
                self.__code__ = func.__code__
                self.__doc__ = func.__doc__
                self.__name__ = func.__name__
                self.__qualname__ = func.__qualname__
                self.__defaults__ = func.__defaults__
                self.__annotations__ = func.__annotations__
                self.__kwdefaults__ = func.__kwdefaults__

                self._wrapped_func: Optional[Callable] = func
                self._function_map: Dict[Tuple[Any, Any], Callable] = {}
            else:
                self._args: Any = args
                self._kwargs: Any = kwargs
        except AttributeError:
            raise TypeError("'cure.decorator' must wrap a function as argument or decorator")

    def __repr__(self) -> str:
        id_ = hex(id(self))
        if getattr(self, "_meta", False) or not getattr(self, "_wrapped_func", None):
            return f"<cure.decorator object at {id_}>"

        id_ = hex(id(getattr(self, "_wrapped_func", None)))
        qualname = getattr(self, "__qualname__", "")
        return f"<function {qualname} at {id_}>"

    @classmethod
    def _args_is_decorated_function(cls, *args: Any, **kwargs: Any) -> bool:
        func: Any = None
        if (
            args
            and not kwargs
            and len(args) == 1
            and (
                callable(args[0])
                or (isinstance(args[0], (staticmethod, classmethod)) and not isinstance(args[0], types.FunctionType))
            )
        ):
            func = args[0]

        if func is not None:
            if not isinstance(func, types.FunctionType) and isinstance(args[0], (staticmethod, classmethod)):
                func.__func__
            return True

        return False

    def __get__(self, instance: Any, owner: Any) -> Callable:
        key = (instance, owner)
        function_map = cast(Dict[Tuple[Any, Any], Callable], getattr(self, "_function_map", {}))
        if key in function_map:
            return function_map[key]

        def partial(func: Callable) -> Callable:
            def _func(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            return _func

        func = partial(self.__call__)
        wrapped_func = cast(Callable, getattr(self, "_wrapped_func", None))
        update_wrapper(func, wrapped_func)

        if getattr(self, "_classmethod", False):
            func = cast(types.FunctionType, func).__get__(owner, None)
        elif not getattr(self, "_staticmethod", False) and instance is not None:
            func = cast(types.FunctionType, func).__get__(instance, None)

        function_map[key] = func
        return func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        wrapped_func = cast(Optional[Callable], getattr(self, "_wrapped_func", None))

        if wrapped_func is None:
            if not getattr(self, "_meta", False) and not self._args_is_decorated_function(*args, **kwargs):
                raise TypeError("'cure.decorator' must wrap a function as argument or decorator")

            result = DecoratorBaseClass(*args, **kwargs)
            if getattr(result, "_wrapped_func", None):
                result._args = getattr(self, "_args", ())
                result._kwargs = getattr(self, "_kwargs", {})

            return result

        trailed_kwargs = {cure.trail(k): v for k, v in kwargs.items()}
        return wrapped_func(*args, **trailed_kwargs)


#        return_value = (await routine) if isinstance(routine, Awaitable) else routine
#        return return_value


class cure(DecoratorBaseClass):
    __version__: str = __version__  # noqa
    __version_info__: Tuple[int, int, int] = __version_info__  # noqa
    __author__: str = __author__
    __email__: str = __email__

    decorator: DecoratorBaseClass

    respected_keywords: set = set(dir(builtins)) | set(keyword.kwlist)

    @staticmethod
    def trail(kw: str) -> str:
        if kw in cure.respected_keywords:
            return f"{kw}_"
        return kw

    def __new__(cls, *args: Any) -> "cure":
        result = cast(cure, object.__new__(cls, *args))
        result._meta = True

        result.decorator = DecoratorBaseClass()
        result.decorator._meta = True

        return result

    def __getitem__(self, item: Any) -> Any:
        raise TypeError("argument of type 'module' is not iterable")


sys.modules[__name__] = cure()  # type: ignore
