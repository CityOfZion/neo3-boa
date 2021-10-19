from typing import Any, Dict, List, Optional, Sized, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class AppendMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.model.type.type import Type
            self_arg = Variable(Type.mutableSequence)
            item_arg = Variable(Type.any)
        else:
            self_arg = Variable(sequence_type)
            item_arg = Variable(sequence_type.value_type)

        identifier = 'append'
        args: Dict[str, Variable] = {'self': self_arg, 'item': item_arg}
        super().__init__(identifier, args)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def stores_on_slot(self) -> bool:
        return True

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
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.OVER, b''),
            (Opcode.ISTYPE, Type.bytearray.stack_item),     # append opcode only works for array
            (Opcode.JMPIFNOT, Integer(5).to_byte_array(min_length=1)),  # when it's bytearray, concatenates the value
            (Opcode.CAT, b''),
            (Opcode.JMP, Integer(5).to_byte_array(min_length=1)),
            (Opcode.APPEND, b'')
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
        if isinstance(value, Sized) and len(value) > 0:
            value = value[0]
        if value == self.args['self'].type:
            return self
        if isinstance(value, MutableSequenceType):
            return AppendMethod(value)
        return super().build(value)
