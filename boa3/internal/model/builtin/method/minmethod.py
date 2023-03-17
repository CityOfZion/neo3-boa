from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class MinMethod(IBuiltinMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'min'

        self._allowed_types = [Type.int, Type.str, Type.bytes]
        default_type = Type.int
        if not self._is_valid_type(arg_value):
            arg_value = default_type

        args: Dict[str, Variable] = {
            'args1': Variable(arg_value),
            'args2': Variable(arg_value)
        }
        vararg = ('values', Variable(arg_value))
        super().__init__(identifier, args, return_type=arg_value, vararg=vararg)

    def _is_valid_type(self, arg_type: Optional[IType]) -> bool:
        return (isinstance(arg_type, IType) and
                any(allowed_type.is_type_of(arg_type) for allowed_type in self._allowed_types))

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_values.type is Type.int:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_values.type._identifier)

    @property
    def _arg_values(self) -> Variable:
        return self._vararg[1]

    @property
    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, SequenceType)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.neo.vm.type.Integer import Integer

        jmp_place_holder = (Opcode.JMP, b'\x01')

        verify_number_of_parameters = [  # verifies if the stack has 2 or 3 items
            (Opcode.DEPTH, b''),
            (Opcode.PUSH2, b''),
            (Opcode.JMPEQ, b''),
            jmp_place_holder
        ]

        if_n_parameters_gt_2 = [  # if number of items in stack is 3
            (Opcode.REVERSE3, b''),
            (Opcode.UNPACK, b''),
            (Opcode.INC, b''),
            (Opcode.INC, b''),
            jmp_place_holder  # skips the next block of instructions
        ]

        if_n_parameters_eq_2 = [  # if number of items in stack is 2
            (Opcode.PUSH2, b'')
        ]

        jmp_n_parameters_eq_2 = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(if_n_parameters_eq_2), True)
        if_n_parameters_gt_2[-1] = jmp_n_parameters_eq_2

        jmp_n_parameters_gt_2 = OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(if_n_parameters_gt_2))
        verify_number_of_parameters[-1] = jmp_n_parameters_gt_2

        repack_array = [  # pack all the arguments in the array
            (Opcode.PACK, b''),
        ]

        is_int_initialize = [  # puts the last array element as the max value
            (Opcode.DUP, b''),  # index = len(array) - 1
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.PICKITEM, b''),     # min = array[index]
        ]

        is_int_while = [    # this will get the next number in the array and compare it with the current min
            (Opcode.SWAP, b''),         # index--
            (Opcode.DEC, b''),
            (Opcode.SWAP, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),         # min = min if min < array[index] else array[index]
            (Opcode.PICKITEM, b''),
        ]
        is_int_while.extend(self._compare_values())
        is_int_while.extend([
            (Opcode.OVER, b''),
            (Opcode.SIGN, b'')
            # if index != 0: go back to index--
            # else go to the end
        ])

        jmp_back_to_while_statement = (Opcode.JMPIF, Integer(-get_bytes_count(is_int_while)).to_byte_array(signed=True))
        is_int_while.append(jmp_back_to_while_statement)

        clean_stack = [    # removes everything but min
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        return (
            verify_number_of_parameters +
            if_n_parameters_gt_2 +
            if_n_parameters_eq_2 +
            repack_array +
            is_int_initialize +
            is_int_while +
            clean_stack
        )

    def _compare_values(self) -> List[Tuple[Opcode, bytes]]:
        return [(Opcode.MIN, b'')]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and len(value) > 0:
            value = value[0]
        if isinstance(value, TupleType):
            value = value.value_type
        if type(value) == type(self._arg_values.type):
            return self

        from boa3.internal.model.builtin.method.minbytestringmethod import MinByteStringMethod
        from boa3.internal.model.builtin.method.minintmethod import MinIntMethod
        from boa3.internal.model.type.type import Type

        if Type.str.is_type_of(value) or Type.bytes.is_type_of(value):
            return MinByteStringMethod(value)

        return MinIntMethod(value)
