from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ExtendMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        from boa3.model.type.type import Type
        if not isinstance(sequence_type, MutableSequenceType):
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        item_arg = Variable(Type.sequence.build_collection(sequence_type.value_type))

        identifier = 'extend'
        args: Dict[str, Variable] = {'self': self_arg, 'item': item_arg}
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
        iterator_type: IType = params[1].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        if not isinstance(iterator_type, SequenceType):
            return False
        return sequence_type.value_type.is_type_of(iterator_type.value_type)

    @property
    def stores_on_slot(self) -> bool:
        return True

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.StackItem import StackItemType
        return [
            (Opcode.OVER, b''),
            (Opcode.ISTYPE, StackItemType.Array),
            (Opcode.JMPIF, Integer(5).to_byte_array(signed=True, min_length=1)),
            (Opcode.CAT, b''),
            (Opcode.JMP, Integer(18).to_byte_array(signed=True, min_length=1)),
            (Opcode.UNPACK, b''),       # get the values, top of stack will be the array size
            (Opcode.JMP, Integer(9).to_byte_array(signed=True, min_length=1)),  # begin while
            (Opcode.DUP, b''),
            (Opcode.INC, b''),          # push the array to the top of the stack
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.ROLL, b''),         # get the first value that wasn't appended yet
            (Opcode.APPEND, b''),       # append the value to the array
            (Opcode.DEC, b''),
            (Opcode.DUP, b''),          # when the array is empty, stop the loop
            (Opcode.JMPIF, Integer(-8).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),  # the top items in the stack will be the extended array and the other array size (zero)
            (Opcode.DROP, b'')
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
            return ExtendMethod(value)
        return super().build(value)
