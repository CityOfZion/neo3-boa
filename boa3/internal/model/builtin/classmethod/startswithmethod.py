import ast
from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StartsWithMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            self_type = Type.bytes

        identifier = 'startswith'
        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'value': Variable(self_type),
            'start': Variable(Type.int),
            'end': Variable(Type.optional.build(Type.int)),
        }

        start_default = ast.parse("{0}".format(0)
                                  ).body[0].value
        end_default = ast.parse("{0}".format(Type.none.default_value)
                                ).body[0].value

        super().__init__(identifier, args, defaults=[start_default, end_default], return_type=Type.bool)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # fix start and end indexes if they are negative or greater than len(string)
        code_generator.swap_reverse_stack_items(4)
        code_generator.swap_reverse_stack_items(3)
        code_generator.fix_negative_index()
        code_generator.swap_reverse_stack_items(2)

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        if_end_is_none = code_generator.convert_begin_if()
        code_generator.change_jump(if_end_is_none, Opcode.JMPIFNOT)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        else_end_is_not_none = code_generator.convert_begin_else(if_end_is_none, is_internal=True)
        code_generator.fix_negative_index()
        code_generator.convert_end_if(else_end_is_not_none, is_internal=True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.fix_index_out_of_range(True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.fix_index_out_of_range(True)

        # if start < len(string):
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        if_start_lt_string_len = code_generator.convert_begin_if()
        code_generator.change_jump(if_start_lt_string_len, Opcode.JMPGE)

        #   string = string[start:end]
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.convert_get_substring(is_internal=True)

        #   if len(string) <= len(substring):
        code_generator.convert_literal(0)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        #       return string[0:len(substring)] == substring
        if_str_is_not_smaller_than_substr = code_generator.convert_begin_if()
        code_generator.change_jump(if_str_is_not_smaller_than_substr, Opcode.JMPGT)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)

        #   elif len(string) > len(substring):
        else_str_is_smaller = code_generator.convert_begin_else(if_str_is_not_smaller_than_substr, is_internal=True)

        for _ in self.args:
            code_generator.remove_stack_top_item()
        #   return False
        code_generator.convert_literal(False)

        code_generator.convert_end_if(else_str_is_smaller, is_internal=True)

        # elif start >= len(string):
        else_start_gt_string_len = code_generator.convert_begin_else(if_start_lt_string_len, is_internal=True)
        for _ in self.args:
            code_generator.remove_stack_top_item()
        #   return False
        code_generator.convert_literal(False)

        code_generator.convert_end_if(else_start_gt_string_len, is_internal=True)

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
            return StartsWithMethod(value)
        return super().build(value)
