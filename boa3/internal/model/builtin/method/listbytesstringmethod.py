from typing import Dict

from boa3.internal.model.builtin.method.listmethod import ListMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ListBytesStringMethod(ListMethod):

    def __init__(self, value: IType = None):
        from boa3.internal.model.type.type import Type

        if value is None:
            value = Type.bytes

        args: Dict[str, Variable] = {
            'value': Variable(value),
        }

        return_type = Type.list.build_collection(value if value is Type.str else Type.int)

        super().__init__(args, return_type)

    def generate_pack_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type

        # index = len(value) - 1
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)

        # while index >= 0
        start_address = code_generator.convert_begin_while()

        #   value[index] to stack
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_item(index_inserted_internally=True)

        if self._arg_value.type is Type.str:
            code_generator.convert_cast(Type.str, is_internal=True)

        #   reorganize stack
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.insert_opcode(Opcode.DEC)

        #   while condition
        condition_address = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.SIGN)
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)

        code_generator.convert_end_while(start_address, condition_address, is_internal=True)

        # clear stack
        code_generator.remove_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
