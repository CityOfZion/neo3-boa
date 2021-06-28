from typing import Dict, List, Optional, Tuple, Any

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.collection.sequence.sequencetype import SequenceType
from boa3.model.type.collection.sequence.tupletype import TupleType
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class MaxMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.model.type.type import Type
        identifier = 'max'
        allowed_types = Type.union.build([Type.int])
        if not isinstance(arg_value, IType):
            arg_value = allowed_types

        args: Dict[str, Variable] = {}
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=arg_value, vararg=vararg)
        self._allowed_types = allowed_types

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.Integer import Integer

        recreate_array = [  # recreates the array to not change the referenced parameter
            (Opcode.UNPACK, b''),
            (Opcode.PACK, b'')
        ]

        if_int_initialize = [   # puts the last array element as the max value
            (Opcode.DUP, b''),          # index = len(array) - 1
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),     # max = array[index]
        ]

        if_int_while = [    # this will get the next number in the array and compare it with the current max
            (Opcode.SWAP, b''),         # index--
            (Opcode.DEC, b''),
            (Opcode.SWAP, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),         # max = max if max > array[index] else array[index]
            (Opcode.PICKITEM, b''),
            (Opcode.MAX, b''),
            (Opcode.OVER, b''),
            (Opcode.SIGN, b'')
            # if index != 0: go back to index--
            # else go to the end
        ]

        jmp_back_to_while_statement = (Opcode.JMPIF, Integer(-get_bytes_count(if_int_while)).to_byte_array(signed=True))
        if_int_while.append(jmp_back_to_while_statement)

        clean_stack = [    # removes everything but max
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        return (
            recreate_array +
            if_int_initialize +
            if_int_while +
            clean_stack
        )

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) == 1:
            value = value[0]
        if isinstance(value, TupleType):
            value = value.value_type
        if type(value) == type(self._arg_values.type):
            return self
        return MaxMethod(value)
