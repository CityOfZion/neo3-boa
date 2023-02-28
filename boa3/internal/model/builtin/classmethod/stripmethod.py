import ast
from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StripMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            from boa3.internal.model.type.primitive.bytestringtype import ByteStringType
            self_type = ByteStringType.build()

        identifier = 'strip'
        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'chars': Variable(self_type),
        }

        from string import whitespace

        # whitespace is ' \t\n\r\v\f', but it needs to be r' \t\n\r\v\f'
        # encode('unicode-escape') will make it a bytes equivalent of r' \t\n\r\v\f' and
        # decode() will convert it back to str
        whitespace_chars = [char.encode('unicode-escape').decode() for char in whitespace]

        if Type.str.is_type_of(self_type):
            chars_default = ast.parse("'{0}'".format(''.join(whitespace_chars))).body[0].value
        else:
            chars_default = ast.parse("b'{0}'".format(''.join(whitespace_chars))).body[0].value

        super().__init__(identifier, args, defaults=[chars_default], return_type=self_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        jmp_place_holder = (Opcode.JMP, b'\x01')

        # receive: string, chars

        initializing_first_loop = [          # initializes the variables for the first loop
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),              # string_size = len(string)
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSH0, b''),             # index = 0
        ]

        verify_leading_chars = [             # verifies if all leading characters are in chars
            (Opcode.DUP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            jmp_place_holder,                # if index >= string_size, jump to initialize_second_loop
        ]

        get_leading_char_at_index = [        # gets the character at the current index and create another index variable
            (Opcode.PUSH4, b''),             # to go through the chars
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),            # char = string[index]
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.PUSH0, b''),             # index_chars = 0
        ]

        verify_if_index_gt_len_chars = [     # verify if already compared all chars with char
            (Opcode.DUP, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            jmp_place_holder,                # if index >= string_size, jump to remove_extras
        ]

        verify_if_char_in_chars = [  # compares char with chars[index_chars]
            (Opcode.PUSH5, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.NUMEQUAL, b''),          # equal = char == chars[index_chars]
            (Opcode.SWAP, b''),
            (Opcode.INC, b''),               # index_chars++
            (Opcode.SWAP, b''),
            # jump back to verify_if_index_gt_len_chars if not equal
        ]

        jmp_back_to_verify_index = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT,
                                                                  -get_bytes_count(verify_if_char_in_chars +
                                                                                   verify_if_index_gt_len_chars))
        verify_if_char_in_chars.append(jmp_back_to_verify_index)

        leading_char_found = [               # char is in chars, so go back to verify_leading_chars
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.INC, b''),               # index++
            # jump back to verify_leading_chars
        ]

        jmp_back_to_verify_leading_chars = OpcodeHelper.get_jump_and_data(Opcode.JMP,
                                                                          -get_bytes_count(verify_leading_chars +
                                                                                           get_leading_char_at_index +
                                                                                           verify_if_index_gt_len_chars +
                                                                                           verify_if_char_in_chars +
                                                                                           leading_char_found))

        leading_char_found.append(jmp_back_to_verify_leading_chars)

        jmp_to_leading_chars = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, get_bytes_count(verify_if_char_in_chars +
                                                                                            leading_char_found), True)
        verify_if_index_gt_len_chars[-1] = jmp_to_leading_chars

        remove_extras = [                   # remove opcodes that won't be used anymore
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        jmp_to_leading_chars = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, get_bytes_count(get_leading_char_at_index +
                                                                                            verify_if_index_gt_len_chars +
                                                                                            verify_if_char_in_chars +
                                                                                            leading_char_found +
                                                                                            remove_extras), True)
        verify_leading_chars[-1] = jmp_to_leading_chars

        get_number_of_leading_chars = (
            initializing_first_loop +
            verify_leading_chars +
            get_leading_char_at_index +
            verify_if_index_gt_len_chars +
            verify_if_char_in_chars +
            leading_char_found +
            remove_extras
        )

        initialize_second_loop = [          # initializes the variables for the second loop
            (Opcode.REVERSE3, b''),         # n_leading = index
            (Opcode.DEC, b''),              # index = string_size - 1
        ]

        verify_trailing_chars = [           # verifies if leading and trailing characters are the same
            (Opcode.DUP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            jmp_place_holder,               # if index <= n_leading, go strip the string
        ]

        get_trailing_char_at_index = [      # gets the character at the current index and create another index variable
            (Opcode.PUSH4, b''),            # to go through the chars
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),           # char = string[index]
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.PUSH0, b''),            # index_chars = 0
        ]

        get_trailing_char_at_index.extend(verify_if_index_gt_len_chars)
        get_trailing_char_at_index.extend(verify_if_char_in_chars)

        trailing_char_found = [             # char is in chars, so go back to get_trailing_char_at_index
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.DEC, b''),              # index--
            # jump back to get_trailing_char_at_index
        ]

        jmp_back_to_verify_trailing_chars = OpcodeHelper.get_jump_and_data(Opcode.JMP,
                                                                           -get_bytes_count(get_trailing_char_at_index +
                                                                                            trailing_char_found))

        trailing_char_found.append(jmp_back_to_verify_trailing_chars)

        remove_extras = [                   # remove opcodes that won't be used anymore
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        jmp_to_strip_string = OpcodeHelper.get_jump_and_data(Opcode.JMPLE, get_bytes_count(get_trailing_char_at_index +
                                                                                           trailing_char_found +
                                                                                           remove_extras), True)
        verify_trailing_chars[-1] = jmp_to_strip_string

        get_number_of_trailing_chars = (
            initialize_second_loop +
            verify_trailing_chars +
            get_trailing_char_at_index +
            trailing_char_found +
            remove_extras
        )

        strip_string = [                    # strips the string using chars
            (Opcode.NIP, b''),
            (Opcode.OVER, b''),
            (Opcode.SUB, b''),
            (Opcode.INC, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.SWAP, b''),
            (Opcode.SUBSTR, b''),           # string.strip(chars)
            (Opcode.CONVERT, StackItemType.ByteString),
        ]

        return (
            get_number_of_leading_chars +
            get_number_of_trailing_chars +
            strip_string
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
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, IByteStringType):
            return StripMethod(value)
        return super().build(value)
