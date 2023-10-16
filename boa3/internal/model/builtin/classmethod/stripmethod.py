import ast
from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StripMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            self_type = Type.bytes

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

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # Initialize first main loop to check the leading characters
        code_generator.duplicate_stack_item(2)
        # string_size = len(string)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        # chars_size = len(chars)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        # index = 0
        code_generator.convert_literal(0)
        # stop_loop = False
        code_generator.convert_literal(False)

        # while index < string_size and not stop_loop:
        while_checking_all_leading_chars = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(5)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        #   char = string[index]
        code_generator.convert_get_substring(is_internal=True)
        #   index_chars = 0
        code_generator.convert_literal(0)

        #   while index < string_size:
        while_checking_leading_char = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(6)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.duplicate_stack_item(3)
        #       equal = char == chars[index_chars]
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        code_generator.swap_reverse_stack_items(2)
        #       index_chars += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)
        #       if equal:
        if_leading_char_is_ws = code_generator.convert_begin_if()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #           index += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.convert_literal(False)
        #           stop_loop = False
        #           break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_leading_char_is_ws)

        while_condition_leading_chars = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.duplicate_stack_top_item()
        #       if index >= string_size:
        if_leading_char_is_not_ws = code_generator.convert_begin_if()
        code_generator.change_jump(if_leading_char_is_not_ws, Opcode.JMPIF)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #           stop_loop = True
        code_generator.convert_literal(True)
        #           break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_leading_char_is_not_ws)
        code_generator.convert_end_while(while_checking_leading_char, while_condition_leading_chars, is_internal=True)

        while_condition_all_leading_chars = code_generator.bytecode_size
        #   if stop_loop:
        if_stop_while = code_generator.convert_begin_if()
        #       break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_stop_while, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.convert_end_while(while_checking_all_leading_chars, while_condition_all_leading_chars, is_internal=True)

        # Initialize second main loop to check the leading characters
        # n_leading = index
        code_generator.swap_reverse_stack_items(3)
        # index = string_size - 1
        code_generator.insert_opcode(Opcode.DEC)
        # stop_loop = False
        code_generator.convert_literal(False)

        # while index > string_size and not stop_loop
        while_checking_all_trailing_chars = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(5)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        #   char = string[index]
        code_generator.convert_get_substring(is_internal=True)
        #   index_chars = 0
        code_generator.convert_literal(0)

        #   while index < string_size:
        while_checking_trailing_char = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(6)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.duplicate_stack_item(3)
        #       equal = char == chars[index_chars]
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        code_generator.swap_reverse_stack_items(2)
        #       index_chars += 1
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)
        #       if equal:
        if_trailing_char_is_ws = code_generator.convert_begin_if()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #           index -= 1
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(False)
        #           stop_loop = False
        #           break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_trailing_char_is_ws)

        while_condition_trailing_chars = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.duplicate_stack_top_item()
        #       if index >= string_size:
        if_trailing_char_is_not_ws = code_generator.convert_begin_if()
        code_generator.change_jump(if_trailing_char_is_not_ws, Opcode.JMPIF)
        # remove_extras
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #           stop_loop = True
        code_generator.convert_literal(True)
        #           break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_trailing_char_is_not_ws)
        code_generator.convert_end_while(while_checking_trailing_char, while_condition_trailing_chars, is_internal=True)

        while_condition_all_trailing_chars = code_generator.bytecode_size
        #   if stop_loop:
        if_stop_while = code_generator.convert_begin_if()
        #       break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_stop_while, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)
        code_generator.convert_end_while(while_checking_all_trailing_chars, while_condition_all_trailing_chars, is_internal=True)

        # Strips the string using the indexes found
        code_generator.remove_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.swap_reverse_stack_items(2)
        # string[n_leading:index]
        code_generator.convert_get_substring(is_internal=True)

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
