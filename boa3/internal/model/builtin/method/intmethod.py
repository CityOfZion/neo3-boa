import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class IntMethod(IBuiltinMethod):

    def __init__(self, args: dict[str, Variable] = None, defaults: list[ast.AST] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'int'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.int)

    @property
    def _arg_value(self) -> Variable:
        return self.args['value']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_value.type is Type.int:
            return '-{0}_{1}'.format(self._identifier, Type.int)

        if self._arg_value.type.is_type_of(Type.str) or self._arg_value.type.is_type_of(Type.bytes):
            return '-{0}_{1}'.format(self._identifier, Type.str)

        return self._identifier

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.type.type import Type
        from boa3.internal.model.builtin.builtin import Builtin
        if len(value) == 0 or Type.int.is_type_of(value[0]):
            return Builtin.IntInt

        if Type.str.is_type_of(value[0]) or Type.bytes.is_type_of(value[0]):
            return Builtin.IntByteString
