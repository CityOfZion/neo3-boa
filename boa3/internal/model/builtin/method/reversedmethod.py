from typing import Any, Dict, Iterable, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ReversedMethod(IBuiltinMethod):
    def __init__(self, args_type: SequenceType = None):
        from boa3.internal.model.type.type import Type
        identifier = 'reversed'
        if not isinstance(args_type, SequenceType):
            args_type = Type.sequence

        args: Dict[str, Variable] = {'sequence': Variable(args_type)}

        super().__init__(identifier, args, return_type=Type.reversed)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self.args['sequence'].type is Type.sequence:
            return self.raw_identifier
        return '-{0}_from_{1}'.format(self._identifier, self.args['sequence'].type.identifier)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Iterable) and len(value) > 0:
            value = value[0]

        if not isinstance(value, SequenceType):
            return ReversedMethod()

        if type(value) == type(self.args['sequence'].type):
            return self

        return ReversedMethod(value)

    @property
    def _body(self) -> Optional[str]:
        return

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.model.type.type import Type
        from boa3.internal.compiler.codegenerator import get_bytes_count

        jmp_place_holder = (Opcode.JMP, b'\x01')

        if_statement = [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.str.stack_item),  # if isinstance(arg1, (str, bytes)) continue
            # if not isinstance(arg1, (str, bytes)) will jump into the else_body
        ]

        if_true_body = [    # if isinstance(arg1, (str, bytes)) body will continue until else_body
            (Opcode.NEWARRAY0, b''),  # list_aux = []
            (Opcode.SWAP, b''),
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),       # limit = len(arg)
            (Opcode.PUSH0, b''),      # index = 0
        ]

        while_statement = [           # index and limit will be at the top of the stack
            (Opcode.DUP, b''),        # verifies if index < limit
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.LT, b''),
            jmp_place_holder          # if index >= limit, go to break_opcode
        ]

        while_body = [                # will add every byte or character into the array and increase the index
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT,
             Type.int.stack_item if Type.bytes.is_type_of(self.args['sequence'].type) else Type.str.stack_item),
            (Opcode.APPEND, b''),    # list_aux.append(arg[index])
            (Opcode.INC, b''),       # index++
            # returns to beginning of the while to verify if it index < limit
        ]

        jmp_back_to_while_statement = OpcodeHelper.get_jump_and_data(Opcode.JMP, -get_bytes_count(while_body + while_statement))
        while_body.append(jmp_back_to_while_statement)

        jmp_to_break_body = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(while_body), True)
        while_statement[-1] = jmp_to_break_body

        break_opcode = [        # remove auxiliary values from stack after leaving `while`
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            # skips the else_body, because it's a bytestring value and unpacking and packing are expensive
        ]

        else_body = [    # creates a new array from an array, used when the arg is not a str or bytes value
            (Opcode.UNPACK, b''),
            (Opcode.PACK, b''),
        ]

        jmp_else_body = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(else_body), True)
        break_opcode.append(jmp_else_body)

        if_true_body = if_true_body + while_statement + while_body + break_opcode

        jmp_if_true_body = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(if_true_body))
        if_statement.append(jmp_if_true_body)

        reverse_array = [   # reverse the array
            (Opcode.DUP, b''),
            (Opcode.REVERSEITEMS, b''),     # return reversed(arg)
        ]

        return (
            if_statement +
            if_true_body +
            else_body +
            reverse_array
        )
