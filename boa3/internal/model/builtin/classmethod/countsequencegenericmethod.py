from typing import List, Optional, Tuple

from boa3.internal.model.builtin.classmethod.countsequencemethod import CountSequenceMethod
from boa3.internal.model.type.collection.sequence.sequencetype import SequenceType
from boa3.internal.model.type.itype import IType


class CountSequenceGenericMethod(CountSequenceMethod):

    def __init__(self, sequence_type: Optional[SequenceType] = None, arg_value: Optional[IType] = None):
        super().__init__(sequence_type, arg_value)

    def _generic_verification(self, code_generator) -> Tuple[List[int], List[int]]:
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        jmps_to_inc, jmps_to_condition = super()._generic_verification(code_generator)

        # if value is Array
        code_generator.duplicate_stack_item(4)
        code_generator.insert_type_check(Type.sequence.stack_item)
        is_value_array = code_generator.convert_begin_if()

        #   item = sequence[index]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)

        #   if item is Array
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(Type.sequence.stack_item)
        is_item_array = code_generator.convert_begin_if()

        #       if len(item) == len(value):
        code_generator.duplicate_stack_item(5)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        is_same_size = code_generator.convert_begin_if()
        code_generator.change_jump(is_same_size, Opcode.JMPNE)

        #           inner_index = len(item)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        #           while inner_index > 0
        while_start = code_generator.convert_begin_while()

        #               inner_index -= 1
        code_generator.insert_opcode(Opcode.DEC)

        #               if item[inner_index] != value[inner_index]
        code_generator.duplicate_stack_item(6)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_get_item(index_inserted_internally=True)
        code_generator.convert_operation(BinaryOp.NotEq)

        are_values_different = code_generator.convert_begin_if()
        code_generator.convert_loop_break()
        #                   break

        code_generator.convert_end_if(are_values_different)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # clean stack
        code_generator.remove_stack_item(2)

        #           if inner_index == 0:
        code_generator.convert_literal(0)
        is_equal = code_generator.convert_begin_if()
        code_generator.change_jump(is_equal, Opcode.JMPEQ)

        jmps_to_inc.append(is_equal)
        #               count += 1

        jmp_to_clean_stack = code_generator.convert_begin_if()
        code_generator.change_jump(jmp_to_clean_stack, Opcode.JMP)

        code_generator.convert_end_if(is_same_size, is_internal=True)
        code_generator.convert_end_if(is_item_array)
        code_generator.remove_stack_top_item()

        code_generator.convert_end_if(jmp_to_clean_stack)

        is_value_array = code_generator.convert_begin_else(is_value_array, is_internal=True)
        jmps_to_condition.append(is_value_array)

        return jmps_to_inc, jmps_to_condition
