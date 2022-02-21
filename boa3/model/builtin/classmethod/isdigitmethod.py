from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.type.primitive.ibytestringtype import IByteStringType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class IsDigitMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            from boa3.model.type.primitive.bytestringtype import ByteStringType
            self_type = ByteStringType.build()

        identifier = 'isdigit'
        args: Dict[str, Variable] = {'self': Variable(self_type)}

        super().__init__(identifier, args, return_type=Type.bool)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.StackItem import StackItemType

        number0 = Integer(ord('0')).to_byte_array()
        number9 = Integer(ord('9')).to_byte_array()
        jmp_place_holder = (Opcode.JMP, b'\x01')

        initializing = [                    # initialize auxiliary values
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),              # index = len(string) - 1
            (Opcode.PUSH1, b''),            # isdigit = True
        ]

        verify_empty_string = [             # verifies if string is empty
            (Opcode.OVER, b''),
            (Opcode.PUSHM1, b''),
            jmp_place_holder,               # jump to change_to_false if index == -1
        ]

        skip_first_verify_while = [         # skips the first while verification, since string is not empty
            jmp_place_holder
        ]

        verify_while = [                    # verifies if while is over
            (Opcode.OVER, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder,               # jump to return_bool if index >= len(string)
        ]

        jmp_verify_while = Opcode.get_jump_and_data(Opcode.JMP, get_bytes_count(verify_while), True)
        skip_first_verify_while[-1] = jmp_verify_while

        while_verify_lt_0 = [               # verifies if ord(string[index]) is < ord('0')
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.DUP, b''),
            (Opcode.PUSHDATA1, Integer(len(number0)).to_byte_array() + number0),
            jmp_place_holder,               # if ord(string[index]) < ord('0'), return False
        ]

        while_verify_gt_9 = [               # verifies if ord(string[index]) is > ord('9')
            (Opcode.PUSHDATA1, Integer(len(number9)).to_byte_array() + number9),
            jmp_place_holder,               # if ord(string[index]) > ord('9'), return False
        ]

        while_go_to_verify = [              # decreases index and goes back to verify if there all characters were visited already
            (Opcode.SWAP, b''),
            (Opcode.DEC, b''),              # index--
            (Opcode.SWAP, b''),
            # jump back to verify_while
        ]

        jmp_back_to_verify = Opcode.get_jump_and_data(Opcode.JMP, -get_bytes_count(verify_while +
                                                                                   while_verify_lt_0 +
                                                                                   while_verify_gt_9 +
                                                                                   while_go_to_verify))
        while_go_to_verify.append(jmp_back_to_verify)

        jmp_out_of_while = Opcode.get_jump_and_data(Opcode.JMPLT, get_bytes_count(while_verify_gt_9 +
                                                                                  while_go_to_verify), True)
        while_verify_lt_0[-1] = jmp_out_of_while

        drop_char = [                       # remove extra char from stack
            (Opcode.DROP, b'')
        ]

        jmp_to_change_to_false = Opcode.get_jump_and_data(Opcode.JMPGT, get_bytes_count(while_go_to_verify +
                                                                                        drop_char), True)
        while_verify_gt_9[-1] = jmp_to_change_to_false

        change_to_false = [                 # remove True on top of stack and put False
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),
        ]

        jmp_to_return = Opcode.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(skip_first_verify_while +
                                                                               verify_while +
                                                                               while_verify_lt_0 +
                                                                               while_verify_gt_9 +
                                                                               while_go_to_verify +
                                                                               drop_char), True)
        verify_empty_string[-1] = jmp_to_return

        jmp_to_return = Opcode.get_jump_and_data(Opcode.JMPLT, get_bytes_count(while_verify_lt_0 +
                                                                               while_verify_gt_9 +
                                                                               while_go_to_verify +
                                                                               drop_char +
                                                                               change_to_false), True)
        verify_while[-1] = jmp_to_return

        clean_and_return_bool = [           # remove extra values from stack
            (Opcode.NIP, b''),
            (Opcode.NIP, b'')
        ]

        return (
            initializing +
            verify_empty_string +
            skip_first_verify_while +
            verify_while +
            while_verify_lt_0 +
            while_verify_gt_9 +
            while_go_to_verify +
            drop_char +
            change_to_false +
            clean_and_return_bool
        )

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, IByteStringType):
            return IsDigitMethod(value)
        return super().build(value)
