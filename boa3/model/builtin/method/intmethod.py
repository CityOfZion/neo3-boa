import ast
from typing import Any, Dict, List, Optional

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.variable import Variable


class IntMethod(IBuiltinMethod):

    def __init__(self, args: Dict[str, Variable] = None, defaults: List[ast.AST] = None):
        from boa3.model.type.type import Type
        identifier = 'int'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.int)

    @property
    def _arg_value(self) -> Variable:
        return self.args['value']

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type

        if self._arg_value.type is Type.int:
            return '-{0}_{1}'.format(self._identifier, Type.str.identifier + Type.bytes.identifier)

        if self._arg_value.type is Type.str or self._arg_value.type is Type.bytes:
            return '-{0}_{1}'.format(self._identifier, Type.sequence.identifier)

        return self._identifier

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.model.type.type import Type
        from boa3.model.builtin.builtin import Builtin
        if len(value) == 0 or Type.int.is_type_of(value[0]):
            return Builtin.IntInt

        if Type.str.is_type_of(value[0]) or Type.bytes.is_type_of(value[0]):
            return Builtin.IntByteString
