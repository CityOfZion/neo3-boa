from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class InsertMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.internal.model.type.type import Type
            sequence_type = Type.mutableSequence

        self_arg = Variable(sequence_type)
        index_arg = Variable(sequence_type.valid_key)
        item_arg = Variable(sequence_type.value_type)

        identifier = 'insert'
        args: Dict[str, Variable] = {'self': self_arg,
                                     '__index': index_arg,
                                     '__object': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 3:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        sequence_type: IType = params[0].type
        index_type: IType = params[1].type
        value_type: IType = params[2].type

        if not isinstance(sequence_type, MutableSequenceType):
            return False
        return sequence_type.key_type.is_type_of(index_type) and sequence_type.value_type.is_type_of(value_type)

    def validate_negative_arguments(self) -> List[int]:
        return [list(self.args).index('__index')]

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        return [
            # insert(pos, index)
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),     # array
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),     # array[-1]
            (Opcode.DEC, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.PUSH2, b''),    # array.append(array[-1])
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.APPEND, b''),   # for x in range(index + 1, len(array) - 1)
            (Opcode.SWAP, b''),     # x = len(array)
            (Opcode.JMP, Integer(16).to_byte_array(signed=True, min_length=1)),
            (Opcode.DEC, b''),      # x =- 1
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),     # aux = array[x]
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.INC, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.SETITEM, b''),      # array[x] = value
            (Opcode.DUP, b''),          # value = aux
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.GT, b''),
            (Opcode.JMPIF, Integer(-18).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.SWAP, b''),     # array[index] = y
            (Opcode.SETITEM, b''),
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
            return InsertMethod(value)
        return super().build(value)
