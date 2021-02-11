from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class RemoveMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.model.type.type import Type
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        item_arg = Variable(sequence_type.value_type)

        identifier = 'remove'
        args: Dict[str, Variable] = {'self': self_arg,
                                     '__value': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 2:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.model.type.itype import IType
        sequence_type: IType = params[0].type
        value_type: IType = params[1].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        return sequence_type.value_type.is_type_of(value_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.PUSH0, b''),  # need to find the index to use REMOVE opcode
            (Opcode.DUP, b''),      # while index < len(array):
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.GE, b''),
            (Opcode.JMPIF, Integer(13).to_byte_array(signed=True, min_length=1)),
            (Opcode.PUSH2, b''),        # if array[index] == value
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),             # break
            (Opcode.JMPEQ, Integer(5).to_byte_array(signed=True, min_length=1)),
            (Opcode.INC, b''),          # index = index + 1
            (Opcode.JMP, Integer(-16).to_byte_array(signed=True, min_length=1)),
            (Opcode.NIP, b''),
            (Opcode.REMOVE, b''),
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
            return RemoveMethod(value)
        return super().build(value)
