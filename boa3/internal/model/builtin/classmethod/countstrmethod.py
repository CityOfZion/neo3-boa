import ast
from typing import Dict, List, Tuple

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.classmethod.countmethod import CountMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class CountStrMethod(CountMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: Dict[str, Variable] = {
            'self': Variable(Type.str),
            'value': Variable(Type.str),
            'start': Variable(Type.int),
            'end': Variable(Type.union.build([Type.int, Type.none])),
        }

        start_default = set_internal_call(ast.parse("{0}".format(Type.int.default_value)
                                                    ).body[0].value)
        end_default = set_internal_call(ast.parse("{0}".format(Type.none.default_value)
                                                  ).body[0].value)

        super().__init__(args, [start_default, end_default])

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.compiler.codegenerator import get_bytes_count
        from boa3.internal.model.type.type import Type

        jmp_place_holder = (Opcode.JMP, b'\x01')

        # region verify end

        verify_end_null = [     # verifies if end is null
            (Opcode.REVERSE4, b''),
            (Opcode.DUP, b''),
            (Opcode.ISNULL, b''),
            jmp_place_holder
        ]

        end_null = [            # if end is null, end = len(self)
            (Opcode.DROP, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            jmp_place_holder    # skip the other end verifications
        ]

        num_jmp_code = get_bytes_count(end_null)
        jmp_str_end_null_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
        verify_end_null[-1] = jmp_str_end_null_statement

        verify_end_neg = [      # verifies if end is < 0
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder
        ]

        end_neg = [             # if end is < 0, then get the positive equivalent number
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder
        ]

        end_still_neg = [       # if end is still < 0 after adding it to len(self), end = 0
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),
        ]

        num_jmp_code = get_bytes_count(end_still_neg)
        jmp_end_still_neg_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, num_jmp_code, True)
        end_neg[-1] = jmp_end_still_neg_statement

        skip_end_gt_size = [
            jmp_place_holder    # skip the other end verification
        ]

        num_jmp_code = get_bytes_count(end_still_neg + end_neg + skip_end_gt_size)
        jmp_end_neg_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, num_jmp_code, True)
        verify_end_neg[-1] = jmp_end_neg_statement

        verify_end_gt_size = [  # verifies if end >= len(self)
            (Opcode.DUP, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            jmp_place_holder,
        ]

        end_gt_size = [         # if end >= len(self), end = len(self)
            (Opcode.DROP, b''),
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
        ]

        num_jmp_code = get_bytes_count(end_gt_size)
        jmp_end_gt_size_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPLE, num_jmp_code, True)
        verify_end_gt_size[-1] = jmp_end_gt_size_statement

        num_jmp_code = get_bytes_count(end_gt_size + verify_end_gt_size)
        jmp_whole_end_gt_size_statement = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)
        skip_end_gt_size[-1] = jmp_whole_end_gt_size_statement

        num_jmp_code = get_bytes_count(
            end_gt_size + verify_end_gt_size + skip_end_gt_size + end_still_neg + end_neg + verify_end_neg
        )
        jmp_whole_end_gt_size_statement = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code, True)
        end_null[-1] = jmp_whole_end_gt_size_statement

        verify_end = (
            verify_end_null +
            end_null +
            verify_end_neg +
            end_neg +
            end_still_neg +
            skip_end_gt_size +
            verify_end_gt_size +
            end_gt_size
        )

        # endregion

        # region verify start

        verify_start_neg = [    # verifies if start is < 0
            (Opcode.OVER, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder
        ]

        start_neg = [           # if start is < 0, then get the positive equivalent index
            (Opcode.SWAP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),
            (Opcode.ADD, b''),
            (Opcode.DUP, b''),
            (Opcode.PUSH0, b''),
            jmp_place_holder
        ]

        start_still_neg = [     # if start is still < 0 after adding it to len(self), start = 0
            (Opcode.DROP, b''),
            (Opcode.PUSH0, b''),
        ]

        num_jmp_code = get_bytes_count(start_still_neg)
        jmp_str_start_still_neg_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, num_jmp_code, True)
        start_neg[-1] = jmp_str_start_still_neg_statement

        correct_start_position = [  # put start on the correct position
            (Opcode.SWAP, b'')
        ]

        num_jmp_code = get_bytes_count(correct_start_position + start_still_neg + start_neg)
        jmp_str_start_neg_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, num_jmp_code, True)
        verify_start_neg[-1] = jmp_str_start_neg_statement

        verify_start = (
            verify_start_neg +
            start_neg +
            start_still_neg +
            correct_start_position
        )

        # endregion

        # region Count logic

        initialize = [          # initialize variables
            (Opcode.PUSH0, b''),  # count = 0
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIZE, b''),  # substr_size = len(substr)
            (Opcode.SWAP, b''),
        ]

        verify_while = [        # verifies if substr_size + index >= end
            (Opcode.OVER, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.ADD, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            jmp_place_holder
        ]

        count_substring = [     # verifies if self[index: index+substr_size] == substr
            (Opcode.PUSH5, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH4, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.PUSH5, b''),
            (Opcode.PICK, b''),
            (Opcode.NUMEQUAL, b''),
            jmp_place_holder
        ]

        count_plusplus = [      # if self[index: index+substr_size] == substr
            (Opcode.INC, b''),  # count++
        ]

        num_jmp_code = get_bytes_count(count_plusplus)
        jmp_count_plusplus_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPIFNOT, num_jmp_code, True)
        count_substring[-1] = jmp_count_plusplus_statement

        go_back_to_while = [    # go back to while verification
            (Opcode.REVERSE4, b''),
            (Opcode.INC, b''),  # index ++
            (Opcode.REVERSE4, b''),
            # jump back to while
        ]

        num_jmp_code = -get_bytes_count(go_back_to_while + count_plusplus + count_substring + verify_while)
        jmp_back_to_while_statement = OpcodeHelper.get_jump_and_data(Opcode.JMP, num_jmp_code)
        go_back_to_while.append(jmp_back_to_while_statement)

        num_jmp_code = get_bytes_count(go_back_to_while + count_plusplus + count_substring)
        jmp_to_clean_stack_statement = OpcodeHelper.get_jump_and_data(Opcode.JMPGT, num_jmp_code, True)
        verify_while[-1] = jmp_to_clean_stack_statement

        clean_stack = [         # remove auxiliary values
            (Opcode.REVERSE4, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.REVERSE3, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
        ]

        count_logic = (
            initialize +
            verify_while +
            count_substring +
            count_plusplus +
            go_back_to_while +
            clean_stack
        )

        # endregion

        # count string logic is verify_end + verify_start  + count_logic
        return (
            verify_end +
            verify_start +
            count_logic
        )
