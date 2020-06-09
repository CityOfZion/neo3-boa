from typing import Optional

from boa3.model.builtin.classmethod.appendmethod import AppendMethod
from boa3.model.builtin.decorator.builtindecorator import IBuiltinDecorator
from boa3.model.builtin.decorator.publicdecorator import PublicDecorator
from boa3.model.builtin.method.lenmethod import LenMethod
from boa3.model.method import Method
from boa3.model.type.itype import IType


class Builtin:
    @classmethod
    def get_symbol(cls, symbol_id: str) -> Optional[Method]:
        for name, method in vars(cls).items():
            if isinstance(method, IBuiltinDecorator) and method.identifier == symbol_id:
                return method

    @classmethod
    def get_by_self(cls, symbol_id: str, self_type: IType) -> Optional[Method]:
        from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
        for name, method in vars(cls).items():
            if (isinstance(method, IBuiltinMethod)
                    and method.identifier == symbol_id
                    and method.validate_self(self_type)):
                return method

    # builtin method
    Len = LenMethod()

    # python class method
    Append = AppendMethod()

    # builtin decorator
    Public = PublicDecorator()
