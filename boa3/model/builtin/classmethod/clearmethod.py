from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ClearMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.model.type.type import Type
            sequence_type = Type.mutableSequence

        identifier = 'clear'
        args: Dict[str, Variable] = {'self': Variable(sequence_type)}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def stores_on_slot(self) -> bool:
        return True

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, MutableSequenceType)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.bytearray.stack_item),     # append opcode only works for array
            (Opcode.JMPIFNOT, Integer(9).to_byte_array(min_length=1)),  # when it's bytearray, concatenates the value
            (Opcode.DROP, b''),
            (Opcode.PUSHDATA1, b'\x00'),
            (Opcode.CONVERT, Type.bytearray.stack_item),
            (Opcode.JMP, Integer(5).to_byte_array(min_length=1)),
            (Opcode.CLEARITEMS, b'')
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
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, MutableSequenceType):
            return ClearMethod(value)
        return super().build(value)
