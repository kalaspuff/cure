import itertools
import sys
from typing import Any, Callable, Dict, cast

SOURCE_VERSION = itertools.count()


class Builder:
    args = ()
    varargs = ()
    varkw = ()
    defaults = ()
    kwonlyargs = ()
    kwonlydefaults = ()

    def __init__(self, name: str, signature: str, module: Any) -> None:
        self.name = name
        self.signature = self.shortsignature = signature

        if module:
            self.module = module

    def build(self, src_code: str, evaldict: Dict[str, Any], **attributes: Any) -> Callable:
        filename = "<cure-build-{}>".format(str(next(SOURCE_VERSION)))
        src = src_code % vars(self)

        compiled_func = compile(src, filename, "single")
        exec(compiled_func, evaldict)

        func = evaldict[self.name]

        func.__name__ = self.name
        func.__dict__ = {**attributes}
        func.__defaults__ = ()
        func.__kwdefaults__ = None
        func.__annotations__ = None

        try:
            frame = sys._getframe(3)
        except AttributeError:  # pragma: no cover
            callermodule = "?"
        else:
            callermodule = frame.f_globals.get("__name__", "?")

        func.__module__ = getattr(self, "module", callermodule)

        return cast(Callable, func)

    @staticmethod
    def create_callable(
        func_def: str, func_body: str, evaldict: Dict[str, Any], module: Any = None, **attributes: Any
    ) -> Callable:
        name, rest = func_def.strip().split("(", 1)
        name = name.strip()
        signature = rest.strip()[:-1].strip()

        src_code = "def {}({}):\n    {}\n".format(name, signature, func_body.strip())

        return Builder(name, signature, module).build(src_code, evaldict, **attributes)
