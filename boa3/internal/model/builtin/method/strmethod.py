import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class StrMethod(IBuiltinMethod):

    def __init__(self, args: dict[str, Variable] = None, defaults: list[ast.AST] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'str'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.str)

    @property
    def _arg_value(self) -> Variable:
        return self.args['object']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type

        if self._arg_value.type is Type.bool:
            return '-{0}_{1}'.format(self._identifier, Type.bool.identifier)

        if self._arg_value.type is Type.int:
            return '-{0}_{1}'.format(self._identifier, Type.int.identifier)

        if Type.sequence.is_type_of(self._arg_value.type):
            return '-{0}_{1}'.format(self._identifier, Type.sequence.identifier)

        from boa3.internal.model.type.classes.userclass import UserClass
        if isinstance(self._arg_value.type, UserClass):
            return '-{0}_{1}'.format(self._identifier, self._arg_value.type.raw_identifier)

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
        if len(value) > 0:

            if Type.bool.is_type_of(value[0]):
                return Builtin.StrBool

            if Type.int.is_type_of(value[0]):
                return Builtin.StrInt

        return Builtin.StrBytes
