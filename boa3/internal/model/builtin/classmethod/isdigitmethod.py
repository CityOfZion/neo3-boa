from typing import Any, Dict, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IsDigitMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IByteStringType):
            self_type = Type.bytes

        identifier = 'isdigit'
        args: Dict[str, Variable] = {'self': Variable(self_type)}

        super().__init__(identifier, args, return_type=Type.bool)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # index = len(string) - 1
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        # isdigit = True
        code_generator.convert_literal(True)

        # if len(string) > 0:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(-1)
        if_string_not_empty = code_generator.convert_begin_if()
        code_generator.change_jump(if_string_not_empty, Opcode.JMPEQ)

        #   while index >= 0:
        while_str_is_analysed = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal('0')

        #       if ord(string[index]) < ord('0'):
        if_char_lt_0 = code_generator.convert_begin_if()
        code_generator.change_jump(if_char_lt_0, Opcode.JMPGE)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        #           return False
        code_generator.convert_literal(False)
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_char_lt_0, is_internal=True)

        #       elif ord(string[index]) > ord('9'):
        code_generator.convert_literal('9')
        if_char_gt_9 = code_generator.convert_begin_if()
        code_generator.change_jump(if_char_gt_9, Opcode.JMPLE)
        #           return False
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(False)
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_char_gt_9, is_internal=True)

        #       index -= 1
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.swap_reverse_stack_items(2)

        # verify if already passed through the whole string
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)
        code_generator.convert_end_while(while_str_is_analysed, while_condition, is_internal=True)

        # elif len(string) == 0:
        else_string_is_empty = code_generator.convert_begin_else(if_string_not_empty, is_internal=True)
        code_generator.remove_stack_top_item()
        #   return False
        code_generator.convert_literal(False)
        code_generator.convert_end_if(else_string_is_empty, is_internal=True)

        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

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
            return IsDigitMethod(value)
        return super().build(value)
