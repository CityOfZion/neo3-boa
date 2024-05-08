from boa3.internal.model.builtin.method.minmethod import MinMethod
from boa3.internal.model.type.itype import IType


class MinByteStringMethod(MinMethod):

    def __init__(self, arg_value: IType | None = None):
        from boa3.internal.model.type.type import Type
        is_valid_type = Type.str.is_type_of(arg_value) or Type.bytes.is_type_of(arg_value)
        super().__init__(arg_value if is_valid_type else Type.str)

    def _compare_values(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        # if (str1 != str2):
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        if_init_are_not_equal = code_generator.convert_begin_if()
        code_generator.change_jump(if_init_are_not_equal, Opcode.JMPEQ)

        #   min_len_str = min((len(str1), len(str2))
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        self.generate_internal_opcodes(code_generator)
        #   index = 0
        code_generator.convert_literal(0)

        #   while(index <= min_len_str):
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

        #       if (value2 == value1):
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        if_values_not_equal = code_generator.convert_begin_if()
        code_generator.change_jump(if_values_not_equal, Opcode.JMPNE)

        #           index += 1
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.insert_opcode(Opcode.INC)

        #   while condition and end
        condition_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        code_generator.convert_end_while(start_while, condition_address, is_internal=True)

        #   if (index > min_len_str):
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        #       is_str2_min = len(str2) < len(str1)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        #       elif (value1 != value2):
        else_values_are_equal = code_generator.convert_begin_else(if_values_not_equal)
        #           is_str2_min = value1 > value2
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.convert_end_if(else_values_are_equal)

        # elif (str1 == str2):
        else_init_are_equal = code_generator.convert_begin_else(if_init_are_not_equal)
        #   is_str2_min = True
        code_generator.convert_literal(1)
        code_generator.convert_end_if(else_init_are_equal, is_internal=True)

        # if (is_str2_min):
        if_str2_is_min = code_generator.convert_begin_if()
        code_generator.change_jump(if_str2_is_min, Opcode.JMPIF)
        #   return str2
        code_generator.remove_stack_top_item()
        # elif (not is_str2_min):
        else_str1_is_min = code_generator.convert_begin_else(if_str2_is_min, is_internal=True)
        code_generator.remove_stack_item(2)
        #   return str1
        code_generator.convert_end_if(else_str1_is_min)
