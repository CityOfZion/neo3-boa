from typing import Optional

from boa3.internal.model.builtin.method.maxmethod import MaxMethod
from boa3.internal.model.type.itype import IType


class MaxByteStringMethod(MaxMethod):

    def __init__(self, arg_value: Optional[IType] = None):
        from boa3.internal.model.type.type import Type
        is_valid_type = Type.str.is_type_of(arg_value) or Type.bytes.is_type_of(arg_value)
        super().__init__(arg_value if is_valid_type else Type.str)

    def _compare_values(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)

        if_is_equal = code_generator.convert_begin_if()
        code_generator.change_jump(if_is_equal, Opcode.JMPNE)
        # if str1 == str2:
        code_generator.convert_literal(True)
        #   condition = True

        if_is_equal = code_generator.convert_begin_else(if_is_equal, insert_jump=True)
        # else:
        #   limit = min((len(str1), len(str2))
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_builtin_method_call(Builtin.Min, is_internal=True)

        #   index = 0
        code_generator.convert_literal(0)

        #   while index < limit:
        start_while = code_generator.convert_begin_while()

        #       value1 = str1[index]
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)
        code_generator.duplicate_stack_item(2)

        #       value2 = str2[index]
        code_generator.duplicate_stack_item(5)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)

        #       if (value2 != value1):
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        if_values_not_equal = code_generator.convert_begin_if()
        code_generator.change_jump(if_values_not_equal, Opcode.JMPEQ)

        #           condition = value2 > value1
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        #           break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_values_not_equal)

        #       index += 1
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.insert_opcode(Opcode.INC)

        #   while condition and end
        condition_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        while_break = code_generator.convert_end_while(start_while, condition_address)

        #   else:
        while_else = code_generator.bytecode_size
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #       condition = len(str1) > len(str2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.convert_end_loop_else(start_while, while_else, has_else=True)

        code_generator.convert_end_if(while_break, is_internal=True)
        code_generator.convert_end_if(if_is_equal, is_internal=True)

        # if condition is True
        is_condition = code_generator.convert_begin_if()
        #   remove str2 <=> return str1
        code_generator.remove_stack_top_item()

        # else
        is_condition = code_generator.convert_begin_else(is_condition)
        #   remove str1 <=> return str2
        code_generator.remove_stack_item(2)

        code_generator.convert_end_if(is_condition)
