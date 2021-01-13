from typing import Any, Dict, Optional, Sequence

from boa3.model.builtin.interop.enumerator.enumeratortype import EnumeratorType
from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.variable import Variable


class EnumeratorMethod(InteropMethod):

    def __init__(self, return_type: EnumeratorType):
        identifier = '-Enumerator__init__'
        syscall = 'System.Enumerator.Create'

        # neo enumerator accepts array or primitive type, except None
        # since the primitives types here are str, bytes, int, bool and none and both str and bytes are sequences and
        # bool is int, only needed to include int in the union
        from boa3.model.type.type import Type
        args: Dict[str, Variable] = {'entry': Variable(Type.union.build([Type.sequence,
                                                                         Type.int]))}
        super().__init__(identifier, syscall, args, return_type=return_type)

    def validate_parameters(self, *params: IExpression) -> bool:
        return len(params) == 0

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def _entry_arg(self) -> Variable:
        return self.args['entry']

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sequence) and len(value) == 1:
            argument = value[0]
        else:
            argument = value

        if self._entry_arg().type.is_type_of(argument):
            enumerator = EnumeratorType.build(argument)
            if enumerator is not self.return_type:
                return EnumeratorMethod(enumerator)
        return super().build(value)
