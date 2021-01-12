import ast
from typing import Any, Dict, Iterable, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.mutable.mutablesequencetype import MutableSequenceType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class PopMethod(IBuiltinMethod):
    def __init__(self, sequence_type: MutableSequenceType = None):
        if not isinstance(sequence_type, MutableSequenceType):
            from boa3.model.type.type import Type
            sequence_type = Type.mutableSequence

        identifier = 'pop'
        args: Dict[str, Variable] = {'self': Variable(sequence_type),
                                     'index': Variable(sequence_type.valid_key)
                                     }
        # TODO: change when dict.pop is implemented
        index_default = ast.parse("-1").body[0].value.operand
        index_default.n = -1
        super().__init__(identifier, args, defaults=[index_default], return_type=sequence_type.value_type)

    @property
    def is_supported(self) -> bool:
        """
        Verifies if the builtin method is supported by the compiler

        :return: True if it is supported. False otherwise.
        """
        # TODO: remove when bytearray.pop() is implemented
        from boa3.model.type.type import Type
        return not Type.bytearray.is_type_of(self._arg_self.type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) < 0 or len(params) > 2:
            return False

        if any(not isinstance(param, (IExpression, IType)) for param in params):
            return False

        sequence = params[0].type if isinstance(params[0], IExpression) else params[0]
        if not isinstance(sequence, MutableSequenceType):
            return False

        if len(params) > 1:
            value = params[1].type if isinstance(params[1], IExpression) else params[1]
            return sequence.valid_key.is_type_of(value)
        return True

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.neo.vm.type.Integer import Integer
        return [
            (Opcode.DUP, b''),
            (Opcode.SIGN, b''),
            (Opcode.PUSHM1, b''),
            (Opcode.JMPNE, Integer(5).to_byte_array(min_length=1, signed=True)),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.SWAP, b''),
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
        if isinstance(value, Iterable) and len(value) > 0:
            if len(value) == 1:
                value = value[0]
            elif self.validate_parameters(*value):
                return PopMethod(value[0])

        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, MutableSequenceType):
            return PopMethod(value)
        return super().build(value)
