import ast
from typing import Dict

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.classmethod.countmethod import CountMethod
from boa3.internal.model.variable import Variable


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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        # if end is None
        code_generator.swap_reverse_stack_items(4)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_operation(BinaryOp.IsNone, is_internal=True)

        verify_end_none = code_generator.convert_begin_if()

        #   end = len(self)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.convert_end_if(verify_end_none)

        # if end < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)

        verify_end_neg = code_generator.convert_begin_if()
        code_generator.change_jump(verify_end_neg, Opcode.JMPGE)

        #   end += len(self)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)

        #   if end < 0:
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)

        verify_end_still_neg = code_generator.convert_begin_if()
        code_generator.change_jump(verify_end_still_neg, Opcode.JMPGE)

        #       end = 0
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(0)

        code_generator.convert_end_if(verify_end_still_neg, is_internal=True)

        # else:
        verify_end_neg = code_generator.convert_begin_else(verify_end_neg, is_internal=True)

        #   if end > len(self)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(5)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        verify_gt_size = code_generator.convert_begin_if()
        code_generator.change_jump(verify_gt_size, Opcode.JMPLE)

        #       end = len(self)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        code_generator.convert_end_if(verify_gt_size)
        code_generator.convert_end_if(verify_end_neg)

        # if start < 0
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)

        verify_start_neg = code_generator.convert_begin_if()
        code_generator.change_jump(verify_start_neg, Opcode.JMPGE)

        #   start += len(self)
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)

        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        #   if start < 0:

        verify_start_still_neg = code_generator.convert_begin_if()
        code_generator.change_jump(verify_start_still_neg, Opcode.JMPGE)

        #       start = 0
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(0)

        code_generator.convert_end_if(verify_start_still_neg)
        code_generator.swap_reverse_stack_items(2)

        code_generator.convert_end_if(verify_start_neg)

        # index = count = 0
        code_generator.convert_literal(0)

        # substr_size = len(substr)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.swap_reverse_stack_items(2)

        while_start = code_generator.convert_begin_while()

        # while substr_size + index <= end
        code_generator.duplicate_stack_item(6)
        code_generator.duplicate_stack_item(5)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_get_substring(is_internal=True)

        #   if self[index: index + substr_size] == substr:
        code_generator.duplicate_stack_item(6)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        is_substr = code_generator.convert_begin_if()

        #       count += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.convert_end_if(is_substr, is_internal=True)

        code_generator.swap_reverse_stack_items(4)
        #   index += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(4)

        # while condition
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.LtE, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # clean stack
        code_generator.swap_reverse_stack_items(4)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
