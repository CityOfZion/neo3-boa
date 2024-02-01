import ast
from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ReplaceMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            self_type = Type.bytes

        identifier = 'replace'
        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'old': Variable(self_type),
            'new': Variable(self_type),
            'count': Variable(Type.int),
        }

        count_default = ast.parse("-1").body[0].value.operand
        count_default.n = -1

        super().__init__(identifier, args, defaults=[count_default], return_type=self_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type

        # old_length = len(old)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        # self_length = len(string)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        # self_length = self_length - old_length + 1
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)

        # if count < 0:
        code_generator.move_stack_item_to_top(5)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        if_less_than_zero = code_generator.convert_begin_if()
        code_generator.change_jump(if_less_than_zero, Opcode.JMPGE)

        #     count = self_length
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_top_item()

        code_generator.convert_end_if(if_less_than_zero)

        # index = 0
        code_generator.convert_literal(0)

        # new_string = ""
        code_generator.convert_literal(Type.str.default_value)

        # while index < self_length:
        while_start = code_generator.convert_begin_while()

        #   if self[index:index + old_length] == old and count > 0:
        #   (self[index:index + old_length] == old)
        code_generator.duplicate_stack_item(8)
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(7)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.duplicate_stack_item(7)


        if_substring_matches_old = code_generator.convert_begin_if()
        code_generator.change_jump(if_substring_matches_old, Opcode.JMPNE)

        #   (count > 0)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(0)

        if_count_greater_than_zero = code_generator.convert_begin_if()
        code_generator.change_jump(if_count_greater_than_zero, Opcode.JMPLE)

        #       new_string += new
        code_generator.duplicate_stack_item(7)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        #       index += old_length
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.swap_reverse_stack_items(2)

        #       count -= 1
        code_generator.swap_reverse_stack_items(3)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.swap_reverse_stack_items(3)

        #   else:
        else_substring_matches_old = code_generator.convert_begin_else(if_substring_matches_old)
        code_generator.convert_end_if(if_count_greater_than_zero)

        #       new_string += self[index]
        code_generator.duplicate_stack_item(8)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        #       index += 1
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)

        code_generator.convert_end_if(else_substring_matches_old)

        # end while
        while_condition_start = code_generator.bytecode_size
        # index < self_length
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition_start, is_internal=True)

        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

        code_generator.remove_stack_item(3)
        code_generator.remove_stack_item(3)

        # if old_length > 1:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        if_old_length_greater_than_one = code_generator.convert_begin_if()
        code_generator.change_jump(if_old_length_greater_than_one, Opcode.JMPLE)

        #     new_string += self[-(old_length - 1):]
        code_generator.swap_reverse_stack_items(3)
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.insert_opcode(Opcode.RIGHT, pop_from_stack=True, add_to_stack=[Type.str])
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        else_old_length_greater_than_one = code_generator.convert_begin_else(if_old_length_greater_than_one, is_internal=True)

        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

        code_generator.convert_end_if(else_old_length_greater_than_one)

        # return new_string
        code_generator.convert_cast(Type.str, is_internal=True)

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
            return ReplaceMethod(value)
        return super().build(value)
