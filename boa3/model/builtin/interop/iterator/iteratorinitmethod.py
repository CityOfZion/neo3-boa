from typing import Dict, Optional

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.interop.iterator.iteratortype import IteratorType
from boa3.model.expression import IExpression
from boa3.model.variable import Variable


class IteratorMethod(InteropMethod):

    def __init__(self, return_type: IteratorType):
        identifier = '-Iterator__init__'
        syscall = 'System.Iterator.Create'
        from boa3.model.type.type import Type
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
