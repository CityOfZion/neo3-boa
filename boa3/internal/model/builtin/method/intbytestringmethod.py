import ast

from boa3.internal.model.builtin.method.intmethod import IntMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IntByteStringMethod(IntMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type

        args: dict[str, Variable] = {
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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type

        # if base >= 37:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(37)
        if_base_ge_37 = code_generator.convert_begin_if()
        code_generator.change_jump(if_base_ge_37, Opcode.JMPLT)
        #   assert False
        code_generator.convert_literal(False)
        code_generator.convert_assert()
        code_generator.convert_end_if(if_base_ge_37, is_internal=True)

        # if base == 1:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        if_base_eq_1 = code_generator.convert_begin_if()
        code_generator.change_jump(if_base_eq_1, Opcode.JMPNE)
        #   assert False
        code_generator.convert_literal(False)
        code_generator.convert_assert()
        code_generator.convert_end_if(if_base_eq_1, is_internal=True)

        # if base <= -1:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(-1)
        if_base_le_m1 = code_generator.convert_begin_if()
        code_generator.change_jump(if_base_le_m1, Opcode.JMPGT)
        #   assert False
        code_generator.convert_literal(False)
        code_generator.convert_assert()
        code_generator.convert_end_if(if_base_le_m1, is_internal=True)

        # if value[0] != 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.convert_literal('0')
        if_first_char_ne_0 = code_generator.convert_begin_if()
        code_generator.change_jump(if_first_char_ne_0, Opcode.JMPNE)

        #   base_hint_char = value[1]
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(1)
        code_generator.convert_get_item(index_inserted_internally=True)

        #   base_found = False
        code_generator.convert_literal(False)

        #   # verifies which base user might be using and change to a cleaner version, e.g., ('0b101', 0) becomes ('101', 2)
        self._verify_is_specific_base('b', 2, code_generator)
        self._verify_is_specific_base('B', 2, code_generator)
        self._verify_is_specific_base('o', 8, code_generator)
        self._verify_is_specific_base('O', 8, code_generator)
        self._verify_is_specific_base('x', 16, code_generator)
        self._verify_is_specific_base('X', 16, code_generator)

        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        code_generator.convert_end_if(if_first_char_ne_0, is_internal=True)

        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        # index = len(value) - 1
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)
        code_generator.convert_assert()
        # sum = 0
        code_generator.convert_literal(0)
        # mult = 1
        code_generator.convert_literal(1)

        # while (index >=  0):
        while_start = code_generator.convert_begin_while()

        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.convert_cast(Type.int, is_internal=True)

        #   if ord(value[index]) >= ord('a') :
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(ord('a'))
        if_char_is_lower = code_generator.convert_begin_if()
        code_generator.change_jump(if_char_is_lower, Opcode.JMPLT)

        #       assert ord(value[index]) <= base + 86
        # # the number 86 is being used because adding it to the base will return the valid characters used on that base
        # # e.g., base 11 lets you use the letter 'a', so, 86 + 11 = 97 == ord('a')
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(7)
        code_generator.convert_literal(86)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.convert_operation(BinaryOp.LtE, is_internal=True)
        code_generator.convert_assert()

        #       sum = sum + (ord(value[index]) - 87) * mult
        code_generator.convert_literal(87)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Mul, is_internal=True)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()

        #   elif ord(value[index]) >= ord('A'):
        else_char_is_not_lower = code_generator.convert_begin_else(if_char_is_lower, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(ord('A'))
        if_char_is_upper = code_generator.convert_begin_if()
        code_generator.change_jump(if_char_is_upper, Opcode.JMPLT)

        #       assert ord(value[index]) <= base + 54
        # # the number 54 is being used because adding it to the base will return the valid characters used on that base
        # # e.g., base 11 lets you use the letter 'A', so, 54 + 11 = 65 == ord('A')
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(7)
        code_generator.convert_literal(54)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.convert_operation(BinaryOp.LtE, is_internal=True)
        code_generator.convert_assert()

        #       sum = sum + (ord(value[index]) - 55) * mult
        code_generator.convert_literal(55)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Mul, is_internal=True)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()

        #   else:
        #       assert ord(value[index]) >= ord('0')
        else_char_is_not_upper = code_generator.convert_begin_else(if_char_is_upper, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(ord('0'))
        code_generator.convert_operation(BinaryOp.GtE)
        code_generator.convert_assert()

        #       assert ord(value[index]) < base + ord('0')
        # # if base is equal or less than 10, the char need to be ord('0') <= ord(char) < ord(str(base))
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(7)
        code_generator.convert_literal(ord('0'))
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.convert_operation(BinaryOp.LtE, is_internal=True)
        code_generator.convert_assert()

        #       sum = sum + (ord(value[index]) - ord('0')) * mult
        code_generator.convert_literal(ord('0'))
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Mul, is_internal=True)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()

        code_generator.convert_end_if(else_char_is_not_lower, is_internal=True)
        code_generator.convert_end_if(else_char_is_not_upper, is_internal=True)
        code_generator.swap_reverse_stack_items(3)
        #   index -= 1
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.swap_reverse_stack_items(3)
        code_generator.duplicate_stack_item(5)
        #   mult = mult * base
        code_generator.convert_operation(BinaryOp.Mul, is_internal=True)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)
        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # return sum
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

    def _verify_is_specific_base(self, char: str, corresponding_base: int, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

        # if base_found:
        if_base_was_found = code_generator.convert_begin_if()
        #   pass
        code_generator.convert_literal(True)

        # elif not base_found:
        else_base_was_not_found = code_generator.convert_begin_else(if_base_was_found, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(char)

        #   if char != value[1]:
        if_chars_not_equal = code_generator.convert_begin_if()
        code_generator.change_jump(if_chars_not_equal, Opcode.JMPEQ)
        #       pass
        code_generator.convert_literal(False)

        #   elif char == value[1]:
        else_chars_equal = code_generator.convert_begin_else(if_chars_not_equal, is_internal=True)

        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(corresponding_base)
        code_generator.convert_operation(BinaryOp.Eq, is_internal=True)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Eq, is_internal=True)
        code_generator.convert_operation(BinaryOp.Xor, is_internal=True)
        #       if base == corresponding_base ^ base == 0:   # remove base indicator from ByteString and change to correct base if base is valid
        if_base_was_valid = code_generator.convert_begin_if()

        #           if base == 0:
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(0)
        if_base_is_0 = code_generator.convert_begin_if()
        code_generator.change_jump(if_base_is_0, Opcode.JMPNE)

        #               base = corresponding_base   # e.g., ('0b101', 0) becomes ('0b101', 2)
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(corresponding_base)
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_end_if(if_base_is_0, is_internal=True)

        #           value = value[2:]       # e.g., ('0b101', 2) becomes ('101', 2)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_literal(2)
        code_generator.convert_get_sequence_ending()
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_end_if(if_base_was_valid)

        #       base_found = True
        code_generator.convert_literal(True)
        code_generator.convert_end_if(else_chars_equal)

        code_generator.convert_end_if(else_base_was_not_found)
