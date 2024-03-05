from boa3.internal.model.builtin.math import *
from boa3.internal.model.callable import Callable
from boa3.internal.model.symbol import ISymbol


class Math:

    # python math methods
    Pow = PowMethod()
    Sqrt = SqrtMethod()

    @classmethod
    def all_functions(cls) -> dict[str, Callable]:
        from boa3.internal.model.builtin.builtincallable import IBuiltinCallable

        functions = [
            cls.Pow,
            cls.Sqrt,
        ]

        return {method._identifier: method for method in functions if isinstance(method, IBuiltinCallable)}

    @classmethod
    def get_methods_from_math_lib(cls) -> dict[str, ISymbol]:
        import math
        from inspect import getmembers, isbuiltin

        method_symbols: dict[str, ISymbol] = {}
        all_functions = getmembers(math, isbuiltin)

        for m_id, method in all_functions:
            method_id: str = m_id if m_id in cls.all_functions() else m_id.lower()
            if method_id in cls.all_functions():
                method_symbols[m_id] = cls.all_functions()[method_id]

        return method_symbols
