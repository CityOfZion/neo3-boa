from typing import Any, Dict, List, Optional, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.type.primitive.ibytestringtype import IByteStringType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class UpperMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):

        if not isinstance(self_type, IByteStringType):
            from boa3.model.type.primitive.bytestringtype import ByteStringType
            self_type = ByteStringType.build()

        identifier = 'upper'
        args: Dict[str, Variable] = {'self': Variable(self_type)}

        super().__init__(identifier, args, return_type=self_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.StackItem import StackItemType
        from boa3.neo.vm.type.Integer import Integer

        lower_a = Integer(ord('a')).to_byte_array()
        lower_z = Integer(ord('z')).to_byte_array()
        jmp_place_holder = (Opcode.JMP, b'\x01')

        initializing = [                    # initialize auxiliary values
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSH0, b''),            # index = 0
        ]

        verify_while = [                    # verifies if while is over
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            jmp_place_holder,               # jump to last statement to clean the stack if index >= len(string)
        ]

        get_substring_left = [              # gets the substring to the left of the index
            (Opcode.REVERSE3, b''),
            (Opcode.DUP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),
            (Opcode.LEFT, b''),             # substr_left = string[:index]
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.ROT, b''),
            (Opcode.ROT, b''),
        ]

        get_substring_middle = [            # gets the substring on the index
            (Opcode.OVER, b''),             # TODO: verify if string[index] < c0 when other values are implemented
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),            # modifier = 1, since using upper is only supported with ASCII for now
            (Opcode.SUBSTR, b''),           # substr_middle = string[index:index+modifier]
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.DUP, b''),
            (Opcode.PUSHDATA1, Integer(len(lower_a)).to_byte_array() + lower_a),
            jmp_place_holder,               # jump to get the substring to the right if substr_middle value is lower than 'a'
        ]

        verify_greater_than_z = [           # verifies if substr_middle is between 'a' and 'z'
            (Opcode.DUP, b''),
            (Opcode.PUSHDATA1, Integer(len(lower_z)).to_byte_array() + lower_z),
            jmp_place_holder,               # jump to get the substring to the right if substr_middle value is greater than 'z'
        ]

        swap_lower_to_upper_case = [        # change middle_substr to uppercase equivalent
            (Opcode.PUSHINT8, Integer(32).to_byte_array(signed=True)),
            (Opcode.SUB, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
        ]

        jmp_to_join_substring = Opcode.get_jump_and_data(Opcode.JMPLT, get_bytes_count(verify_greater_than_z +
                                                                                       swap_lower_to_upper_case), True)
        get_substring_middle[-1] = jmp_to_join_substring

        jmp_to_join_substring = Opcode.get_jump_and_data(Opcode.JMPGT, get_bytes_count(swap_lower_to_upper_case), True)
        verify_greater_than_z[-1] = jmp_to_join_substring

        get_substring_middle.extend(verify_greater_than_z)
        get_substring_middle.extend(swap_lower_to_upper_case)

        get_substring_right = [             # gets the substring to the right of the index
            (Opcode.ROT, b''),
            (Opcode.ROT, b''),
            (Opcode.INC, b''),
            (Opcode.NEGATE, b''),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.RIGHT, b''),            # substr_right = string[index+modifier:]
        ]

        join_substrings = [                 # concatenate substr_left, substr_middle, substr_right
            (Opcode.CAT, b''),
            (Opcode.CAT, b''),              # substr_left + substr_middle + substr_right
            (Opcode.NIP, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.REVERSE3, b''),
            (Opcode.INC, b''),              # index ++
            # jump back to verify,
        ]

        jmp_to_verify_while = Opcode.get_jump_and_data(Opcode.JMP, -get_bytes_count(verify_while +
                                                                                    get_substring_left +
                                                                                    get_substring_middle +
                                                                                    get_substring_right +
                                                                                    join_substrings))
        join_substrings.append(jmp_to_verify_while)

        clean_stack = [                     # removes all auxiliary values
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        while_body = (
            get_substring_left +
            get_substring_middle +
            get_substring_right +
            join_substrings
        )

        jmp_to_clean_stack = Opcode.get_jump_and_data(Opcode.JMPLE, get_bytes_count(while_body), True)
        verify_while[-1] = jmp_to_clean_stack

        return (
            initializing +
            verify_while +
            while_body +
            clean_stack
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
            return UpperMethod(value)
        return super().build(value)
