import ast
from typing import Dict, Optional

from boa3.internal.model.builtin.classmethod.indexmethod import IndexMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.type.primitive.strtype import StrType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class IndexBytesStringMethod(IndexMethod):

    def __init__(self, self_type: Optional[StrType] = None):
        from boa3.internal.model.type.type import Type
        if not isinstance(self_type, (StrType, BytesType)):
            self_type = Type.str

        args: Dict[str, Variable] = {
            'self': Variable(self_type),
            'x': Variable(self_type),
            'start': Variable(Type.int),
            'end': Variable(Type.optional.build(Type.int)),
        }

        start_default = ast.parse("{0}".format(0)
                                  ).body[0].value
        end_default = ast.parse("{0}".format(Type.none.default_value)
                                ).body[0].value

        super().__init__(args, defaults=[start_default, end_default])

    def validate_parameters(self, *params: IExpression) -> bool:
        if 2 <= len(params) <= 4:
            return False
        if not all(isinstance(param, IExpression) for param in params):
            return False

        from boa3.internal.model.type.itype import IType
        self_type: IType = params[0].type

        if not isinstance(self_type, (StrType, BytesType)):
            return False

        if not self_type.is_type_of(params[1]):
            return False

        return True

    @property
    def error_message(self) -> str:
        return 'substring not found' if isinstance(self._arg_self.type, StrType) else 'subsequence of bytes not found'

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # fix possible negative or too big indexes for start and end parameters
        code_generator.swap_reverse_stack_items(2)
        code_generator.swap_reverse_stack_items(4)
        code_generator.swap_reverse_stack_items(2)
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
        code_generator.swap_reverse_stack_items(2)

        # change order of items on stack
        code_generator.duplicate_stack_item(4)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        # current_index = start
        # while (size < end - current_index):
        while_start = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.duplicate_stack_item(6)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        #   if str[index:current_index + size] == substr:
        if_was_found = code_generator.convert_begin_if()
        code_generator.change_jump(if_was_found, Opcode.JMPIFNOT)
        #       break
        code_generator.convert_loop_break()
        code_generator.convert_end_if(if_was_found)
        #   current_index += 1
        code_generator.insert_opcode(Opcode.INC)

        condition_address = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)
        code_generator.convert_end_while(while_start, condition_address, is_internal=True)

        # if current_index + size >= end:
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.duplicate_stack_item(4)
        check_was_found = code_generator.convert_begin_if()
        code_generator.change_jump(check_was_found, Opcode.JMPGE)
        #   raise Exception('substring not found')
        code_generator.convert_literal(self.error_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(check_was_found)
        # else:
        #   return current_index
        for _ in range(1, len(code_generator._stack)):
            code_generator.remove_stack_item(2)
