from typing import Any, Dict, Optional, Sequence

from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.variable import Variable


class IteratorMethod(InteropMethod):

    def __init__(self, return_type: IteratorType):
        identifier = '-Iterator__init__'
        syscall = 'System.Iterator.Create'
        from boa3.internal.model.type.type import Type
        args: Dict[str, Variable] = {'entry': Variable(Type.collection)}
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
            iterator = IteratorType.build(argument)
            if iterator is not self.return_type:
                return IteratorMethod(iterator)
        return super().build(value)
