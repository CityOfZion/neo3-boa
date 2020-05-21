from typing import Optional

from boa3.model.builtin.builtinmethod import IBuiltinMethod
from boa3.model.builtin.lenmethod import LenMethod


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id) -> Optional[IBuiltinMethod]:
        for name, method in vars(cls).items():
            if isinstance(method, IBuiltinMethod) and method.identifier == symbol_id:
                return method

    Len = LenMethod()
