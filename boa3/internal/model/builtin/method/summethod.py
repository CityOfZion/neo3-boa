import ast

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class SumMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'sum'
        args: dict[str, Variable] = {'__iterable': Variable(Type.sequence.build_collection(Type.int)),
                                     '__start': Variable(Type.int)}

        start_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value
        super().__init__(identifier, args, defaults=[start_default], return_type=Type.int)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # index = 0
        code_generator.convert_literal(0)

        # while index < len(iterable)
        while_start = code_generator.convert_begin_while()

        code_generator.swap_reverse_stack_items(3)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(4)
        code_generator.convert_get_item(index_inserted_internally=True, test_is_negative_index=False)
        # sum += iterable[index]
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.swap_reverse_stack_items(3)
        # index += 1
        code_generator.insert_opcode(Opcode.INC)

        # while condition and end
        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.convert_end_while(while_start, while_condition, is_internal=True)

        # remove auxiliary values from stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
