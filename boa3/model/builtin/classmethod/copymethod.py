from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.listtype import ListType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class CopyMethod(IBuiltinMethod):
    def __init__(self, self_type: ListType = None):
        from boa3.model.type.type import Type
        if not isinstance(self_type, ListType):
            self_type = Type.list

        identifier = 'copy'

        args: Dict[str, Variable] = {'self': Variable(self_type)}
        super().__init__(identifier, args, return_type=self_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, ListType)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        return [
            (Opcode.UNPACK, b''),
            (Opcode.PACK, b''),
        ]

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if value == self.args['self'].type:
            return self
        if isinstance(value, ListType):
            return CopyMethod(value)
        return super().build(value)
