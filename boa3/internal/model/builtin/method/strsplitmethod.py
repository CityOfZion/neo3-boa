import ast
from typing import Dict, List

from boa3.internal.model.builtin.interop.nativecontract import StdLibMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class StrSplitMethod(StdLibMethod):
    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'split'
        syscall = 'stringSplit'
        args: Dict[str, Variable] = {
            'self': Variable(Type.str),
            'sep': Variable(Type.str),
            'maxsplit': Variable(Type.int)
        }
        # whitespace is the default separator
        separator_default = ast.parse("' '").body[0].value
        # maxsplit the default value is -1
        maxsplit_default = ast.parse("-1").body[0].value.operand
        maxsplit_default.n = -1

        neo_internal_args = {
            'str': Variable(Type.str),
            'separator': Variable(Type.str),
        }

        super().__init__(identifier, syscall, args, defaults=[separator_default, maxsplit_default],
                         return_type=Type.list.build_collection(Type.str),
                         internal_call_args=len(neo_internal_args))

    @property
    def generation_order(self) -> List[int]:
        # the original string must be the top value in the stack
        indexes = list(range(len(self.args)))
        str_index = list(self.args).index('self')

        if indexes[-1] != str_index:
            # context must be the last generated argument
            indexes.remove(str_index)
            indexes.append(str_index)
        return indexes

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        code_generator.duplicate_stack_item(3)
        code_generator.swap_reverse_stack_items(2)
        super().generate_internal_opcodes(code_generator)

        # if maxsplit > 0
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        is_valid_split_count = code_generator.convert_begin_if()
        code_generator.change_jump(is_valid_split_count, Opcode.JMPLT)

        #   while len(array) < maxsplit + 1:
        while_start = code_generator.convert_begin_while()
        code_generator.duplicate_stack_top_item()

        #       concat values
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.insert_opcode(Opcode.POPITEM, pop_from_stack=True)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.insert_opcode(Opcode.POPITEM, pop_from_stack=True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend, is_internal=True)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(3)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        code_generator.convert_end_if(is_valid_split_count, is_internal=True)
        # clean stack

        code_generator.swap_reverse_stack_items(3)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
