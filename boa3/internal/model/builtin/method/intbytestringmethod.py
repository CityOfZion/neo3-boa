import ast
from typing import Dict, List, Tuple

from boa3.internal.model.builtin.method.intmethod import IntMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IntByteStringMethod(IntMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: Dict[str, Variable] = {
            'value': Variable(Type.union.build([
                Type.bytes,
                Type.str
            ])),
            'base': Variable(Type.int)
        }

        value_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value

        base_default = ast.parse("{0}".format(10)
                                 ).body[0].value

        super().__init__(args, [value_default, base_default])

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        jmp_place_holder = (Opcode.JMP, b'\x01')
        a_lower = ord('a')
        a_upper = ord('A')
        zero = ord('0')

        # region verify_base

        verify_base_ge37 = [    # verifies if base >= 37, base greater than 36 shouldn't be accepted
            (Opcode.OVER, b''),
            OpcodeHelper.get_push_and_data(37),
            jmp_place_holder,   # jumps to an assertion error
        ]

        verify_base_equal1 = [  # verifies if base == 1, base equals 1 shouldn't be accepted
            (Opcode.OVER, b''),
            (Opcode.PUSH1, b''),
            jmp_place_holder    # jumps to an assertion error
        ]

        verify_base_le_minus1 = [   # verifies if base <= -1, base less than 0 shouldn't be accepted
            (Opcode.OVER, b''),
            (Opcode.PUSHM1, b''),
            jmp_place_holder,       # jumps to an assertion error
        ]

        verify_base_jump_error = [  # jumps the next set of instructions
            jmp_place_holder
        ]

        verify_base_error = [       # an invalid base was used
            (Opcode.PUSH0, b''),
            (Opcode.ASSERT, b''),
        ]

        # region verify_base jump logic

        jump_instructions = verify_base_error
        verify_base_jump_error[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(jump_instructions), True)

        jump_instructions = verify_base_jump_error
        verify_base_le_minus1[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPLE, get_bytes_count(jump_instructions), True)

        jump_instructions = verify_base_jump_error + verify_base_le_minus1
        verify_base_equal1[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(jump_instructions), True)

        jump_instructions = verify_base_jump_error + verify_base_le_minus1 + verify_base_equal1
        verify_base_ge37[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, get_bytes_count(jump_instructions), True)

        # endregion

        verify_base = (
            verify_base_ge37 +
            verify_base_equal1 +
            verify_base_le_minus1 +
            verify_base_jump_error +
            verify_base_error
        )

        # endregion

        # region verify_code_literal

        verify_code_literal_first_char_is_0 = [     # verifies if the first char in the value is '0'
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            OpcodeHelper.get_pushdata_and_data('0'),
            jmp_place_holder,                       # if first char is not 0, skip all verify_code_literal methods
        ]

        verify_code_literal_remove_first_char = [   # the first char is 0, so it will be removed from the value
            (Opcode.PUSH1, b''),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
        ]

        verify_code_literal_get_base_char = [       # puts the char that could refer to a base in the top of the stack
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
        ]

        verify_code_literal_initialize_verification = [     # puts a False in the top of the stack to assist the
            (Opcode.PUSH0, b'')                             # verifications above
        ]

        verify_code_literal_base_verification = (           # verifies if the original value starts with 0b, 0B, 0o, 0O
            self._verify_is_specific_base('b', 2) +         # 0x, or 0X, and changes the base if necessary
            self._verify_is_specific_base('B', 2) +
            self._verify_is_specific_base('o', 8) +
            self._verify_is_specific_base('O', 8) +
            self._verify_is_specific_base('x', 16) +
            self._verify_is_specific_base('X', 16)
        )

        verify_code_literal_drop_aux = [                    # drops auxiliary values from the stack and just keeps the
            (Opcode.DROP, b''),                             # base and value on it
            (Opcode.DROP, b''),
        ]

        # region verify_code_literal jump logic

        jump_instructions = (
            verify_code_literal_remove_first_char +
            verify_code_literal_get_base_char +
            verify_code_literal_initialize_verification +
            verify_code_literal_base_verification +
            verify_code_literal_drop_aux
        )

        verify_code_literal_first_char_is_0[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPNE_L,
                                                                                 get_bytes_count(jump_instructions), True)

        # endregion

        verify_code_literal = (
            verify_code_literal_first_char_is_0 +
            verify_code_literal_remove_first_char +
            verify_code_literal_get_base_char +
            verify_code_literal_initialize_verification +
            verify_code_literal_base_verification +
            verify_code_literal_drop_aux
        )

        # endregion

        # region ascii to int

        ascii_to_int_initialize = [     # initialize auxiliary variables on the stack
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),          # index = len(value) - 1
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            (Opcode.GE, b''),
            (Opcode.ASSERT, b''),       # verifies if value was empty
            (Opcode.PUSH0, b''),        # sum = 0
            (Opcode.PUSH1, b''),        # mult = 1
        ]

        ascii_to_int_while = [      # loops from left to right of the value to calculate the equivalent sum in base 10
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH1, b''),
            (Opcode.SUBSTR, b''),   # char = value[index]
            (Opcode.CONVERT, StackItemType.Integer),
        ]

        ascii_to_int_verify_az_lower_lt = [     # verifies ord(char) is less than ord('a')
            (Opcode.DUP, b''),                  # if ord(char) is indeed less, go to verify with ord('A')
            OpcodeHelper.get_push_and_data(a_lower),
            jmp_place_holder                    # jump to ascii_to_int_verify_az_upper_lt
        ]

        ascii_to_int_verify_az_lower_gt = [     # verifies ord(char) is greater than base + 86
            (Opcode.DUP, b''),                  # the minimum base that accepts letters is base 11, that's why it's
            (Opcode.PUSH6, b''),                # adding 86
            (Opcode.PICK, b''),                 # if ord(char) is greater than base + 86, the char is invalid
            OpcodeHelper.get_push_and_data(86),
            (Opcode.ADD, b''),
            (Opcode.LE, b''),
            (Opcode.ASSERT, b''),               # if assert is False, then the char was indeed invalid
        ]

        ascii_to_int_verify_az_lower = [        # the char was in between 'a' and 'z',
            OpcodeHelper.get_push_and_data(87),       # so it will be converted to the respective base 10 number
            (Opcode.SUB, b''),
            (Opcode.OVER, b''),
            (Opcode.MUL, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.ADD, b''),                  # sum = sum + (ord(char) - 55)) * mult
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            jmp_place_holder                    # jumps to ascii_to_int_verify_while
        ]

        ascii_to_int_verify_az_upper_lt = [     # verifies ord(char) is less than ord('A')
            (Opcode.DUP, b''),                  # if ord(char) is indeed less, go to verify with ord('0')
            OpcodeHelper.get_push_and_data(a_upper),
            jmp_place_holder                    # jump to ascii_to_int_verify_09_lt
        ]

        ascii_to_int_verify_az_upper_gt = [     # verifies ord(char) is greater than base + 54
            (Opcode.DUP, b''),                  # the minimum base that accepts letters is base 11, that's why it's
            (Opcode.PUSH6, b''),                # adding 54
            (Opcode.PICK, b''),                 # if ord(char) is greater than base + 54, the char is invalid
            OpcodeHelper.get_push_and_data(54),
            (Opcode.ADD, b''),
            (Opcode.LE, b''),
            (Opcode.ASSERT, b''),               # if assert is False, then the char was indeed invalid
        ]

        ascii_to_int_verify_az_upper = [        # the char was in between 'A' and 'Z',
            OpcodeHelper.get_push_and_data(55),       # so it will be converted to the respective base 10 number
            (Opcode.SUB, b''),
            (Opcode.OVER, b''),
            (Opcode.MUL, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.ADD, b''),                  # sum = sum + (ord(char) - 55)) * mult
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            jmp_place_holder                    # jumps to ascii_to_int_verify_while
        ]

        ascii_to_int_verify_09_lt = [           # verifies ord(char) is less than ord('0')
            (Opcode.DUP, b''),                  # if ord(char) is indeed less, the char is invalid
            OpcodeHelper.get_push_and_data(zero),
            (Opcode.GE, b''),
            (Opcode.ASSERT, b''),               # if assert is False, then the char was indeed invalid
        ]

        ascii_to_int_verify_09_gt = [           # verifies ord(char) is greater than base + ord('0')
            (Opcode.DUP, b''),                  # if ord(char) is greater than base + ord('0'), the char is invalid
            (Opcode.PUSH6, b''),
            (Opcode.PICK, b''),
            OpcodeHelper.get_push_and_data(zero),
            (Opcode.ADD, b''),
            (Opcode.LE, b''),
            (Opcode.ASSERT, b''),               # if assert is False, then the char was indeed invalid
        ]

        ascii_to_int_verify_09 = [              # the char was in between '0' and '9',
            OpcodeHelper.get_push_and_data(zero),     # so it will be converted to the respective base 10 number
            (Opcode.SUB, b''),
            (Opcode.OVER, b''),
            (Opcode.MUL, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.ADD, b''),                  # sum = sum + (ord(char) - ord('0')) * mult
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
        ]

        ascii_to_int_verify_while = [           # verifies if the loop already went through all the chars in value
            (Opcode.REVERSE3, b''),
            (Opcode.DEC, b''),                  # index--
            (Opcode.REVERSE3, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.MUL, b''),                  # mult = mult * base
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH0, b''),
            # jmp back to ascii_to_int_while if index >= 0
        ]

        # region ascii to int jump logic

        jump_instructions = (
            ascii_to_int_verify_09_lt +
            ascii_to_int_verify_09_gt +
            ascii_to_int_verify_09
        )

        ascii_to_int_verify_az_upper[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP,
                                                                          get_bytes_count(jump_instructions), True)

        jump_instructions = (
            ascii_to_int_verify_az_upper_gt +
            ascii_to_int_verify_az_upper
        )

        ascii_to_int_verify_az_upper_lt[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPLT,
                                                                             get_bytes_count(jump_instructions), True)

        jump_instructions = (
            ascii_to_int_verify_az_upper_lt +
            ascii_to_int_verify_az_upper_gt +
            ascii_to_int_verify_az_upper +
            ascii_to_int_verify_09_lt +
            ascii_to_int_verify_09_gt +
            ascii_to_int_verify_09
        )

        ascii_to_int_verify_az_lower[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP,
                                                                          get_bytes_count(jump_instructions), True)

        jump_instructions = (
            ascii_to_int_verify_az_lower_gt +
            ascii_to_int_verify_az_lower
        )

        ascii_to_int_verify_az_lower_lt[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPLT,
                                                                             get_bytes_count(jump_instructions), True)

        jump_instructions = (
            ascii_to_int_while +
            ascii_to_int_verify_az_lower_lt +
            ascii_to_int_verify_az_lower_gt +
            ascii_to_int_verify_az_lower +
            ascii_to_int_verify_az_upper_lt +
            ascii_to_int_verify_az_upper_gt +
            ascii_to_int_verify_az_upper +
            ascii_to_int_verify_09_gt +
            ascii_to_int_verify_09_lt +
            ascii_to_int_verify_09 +
            ascii_to_int_verify_while
        )

        ascii_to_int_verify_while.append(OpcodeHelper.get_jump_and_data(Opcode.JMPGE,
                                                                        -get_bytes_count(jump_instructions), True))

        # endregion

        ascii_to_int = (
            ascii_to_int_initialize +
            ascii_to_int_while +
            ascii_to_int_verify_az_lower_lt +
            ascii_to_int_verify_az_lower_gt +
            ascii_to_int_verify_az_lower +
            ascii_to_int_verify_az_upper_lt +
            ascii_to_int_verify_az_upper_gt +
            ascii_to_int_verify_az_upper +
            ascii_to_int_verify_09_lt +
            ascii_to_int_verify_09_gt +
            ascii_to_int_verify_09 +
            ascii_to_int_verify_while
        )

        # endregion

        # region clean stack

        clean_stack = [         # clean everything but the number in base 10
            (Opcode.DROP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
            (Opcode.NIP, b''),
        ]

        # endregion

        return (
            verify_base +
            verify_code_literal +
            ascii_to_int +
            clean_stack
        )

    def _verify_is_specific_base(self, char: str, base: int) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.neo.vm.type.StackItem import StackItemType
        jmp_place_holder = (Opcode.JMP, b'\x01')

        verify_top_stack = [    # verify if True is in the top of the stack
            jmp_place_holder
        ]

        top_stack_is_true = [       # if True is indeed at the top, ignore the rest of this method
            (Opcode.PUSH1, b''),
            jmp_place_holder        # jumps everything below
        ]

        compare_char = [            # compares the char with b, B, o, O, x, or X
            (Opcode.DUP, b''),
            OpcodeHelper.get_pushdata_and_data(char),
            jmp_place_holder
        ]

        char_not_equal = [          # if char at the top of the stack is not b, B, o, O, x, or X,
            (Opcode.PUSH0, b''),    # put False at the top of the stack

            jmp_place_holder        # jumps everything below
        ]

        verify_base_is_the_same = [     # verify if the equivalent base is the same as current base
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            OpcodeHelper.get_push_and_data(base),
            jmp_place_holder            # jump to remove_base_char if equivalent base is the same as current base
        ]

        verify_base_is_0 = [            # verify if the current base is 0
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder            # if base is not 0, jump to put_true_in_stack
        ]

        change_base = [                 # if base was 0, then change it to the equivalent base
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            OpcodeHelper.get_push_and_data(base),
            (Opcode.REVERSE3, b''),
        ]

        remove_base_char = [            # if base was 0 or 16, remove the char in value
            (Opcode.SWAP, b''),
            (Opcode.PUSH1, b''),
            (Opcode.OVER, b''),
            (Opcode.SIZE, b''),
            (Opcode.DEC, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, StackItemType.ByteString),
            (Opcode.SWAP, b''),
        ]

        put_true_in_stack = [           # puts True in the top of the stack to skip the next verifications
            (Opcode.PUSH1, b'')
        ]

        # region jmp logic

        jump_instructions = change_base + remove_base_char
        verify_base_is_0[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPNE, get_bytes_count(jump_instructions), True)

        jump_instructions = change_base + verify_base_is_0
        verify_base_is_the_same[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(jump_instructions), True)

        jump_instructions = change_base + remove_base_char + put_true_in_stack + verify_base_is_0 + verify_base_is_the_same
        char_not_equal[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(jump_instructions), True)

        jump_instructions = char_not_equal
        compare_char[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(jump_instructions), True)

        jump_instructions = (
            compare_char +
            char_not_equal +
            change_base +
            put_true_in_stack +
            verify_base_is_the_same +
            verify_base_is_0 +
            remove_base_char
        )
        top_stack_is_true[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(jump_instructions), True)

        jump_instructions = top_stack_is_true
        verify_top_stack[-1] = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(jump_instructions), True)

        # endregion

        return (
            verify_top_stack +
            top_stack_is_true +
            compare_char +
            char_not_equal +
            verify_base_is_the_same +
            verify_base_is_0 +
            change_base +
            remove_base_char +
            put_true_in_stack
        )
