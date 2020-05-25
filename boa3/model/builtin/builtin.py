from typing import Optional

from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.builtin.decorator.publicdecorator import PublicDecorator
from boa3.model.builtin.method.lenmethod import LenMethod
from boa3.model.method import Method


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id) -> Optional[Method]:
        for name, method in vars(cls).items():
            if isinstance(method, IBuiltinDecorator) and method.identifier == symbol_id:
                return method

    # builtin method
    Len = LenMethod()

    # builtin decorator
    Public = PublicDecorator()
