from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.variable import Variable


class ToHexStrMethod(IBuiltinMethod):

    def __init__(self):
        from boa3.internal.model.type.type import Type
        identifier = 'to_hex_str'
        args: dict[str, Variable] = {
            'data': Variable(Type.bytes)
        }
        super().__init__(identifier, args, return_type=Type.str)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal import constants
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.opcode.Opcode import Opcode

        max_size_to_convert = constants.SIZE_OF_INT256
        hex_base = 16

        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(0)
        # if len(arg) == 0
        is_empty = code_generator.convert_begin_if()
        #   result = arg  # do nothing on script
        # else
        code_generator.change_jump(is_empty, Opcode.JMPEQ)

        #   no_calls = len(arg) // max_size + 1
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(max_size_to_convert)
        code_generator.convert_operation(BinaryOp.IntDiv, is_internal=True)
        code_generator.insert_opcode(Opcode.INC)
        #   result = ''
        code_generator.convert_literal('')
        #   index = 0
        code_generator.convert_literal(0)

        #   while index < no_calls:
        loop_start = code_generator.convert_begin_while()
        code_generator.convert_literal(hex_base)

        code_generator.duplicate_stack_item(5)
        #       pos = index * max_size
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(max_size_to_convert)
        code_generator.convert_operation(BinaryOp.Mul)

        #       subsize = min(len(arg) - pos, max_size)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Sub)
        code_generator.convert_literal(max_size_to_convert)
        code_generator.convert_builtin_method_call(Builtin.Min, is_internal=True)

        code_generator.convert_get_substring(is_internal=True, fix_result_type=False)
        #       aux = itoa(arg[pos: pos + max_size], hex_base)
        code_generator.convert_cast(Type.int, is_internal=True)
        code_generator.convert_builtin_method_call(Interop.Itoa, is_internal=True)

        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(2)
        code_generator.convert_operation(BinaryOp.Mod, is_internal=True)
        #       if len(aux) % 2:
        is_odd = code_generator.convert_begin_if()

        #           aux = '0' + aux
        code_generator.convert_literal('0')
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)

        code_generator.convert_end_if(is_odd)

        code_generator.swap_reverse_stack_items(3, rotate=True)
        #       result += aux
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.swap_reverse_stack_items(2)

        #       index += 1
        code_generator.insert_opcode(Opcode.INC)

        loop_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Gt)

        code_generator.convert_end_while(loop_start, loop_condition, is_internal=True)

        # clear stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

        code_generator.convert_cast(self.return_type)

        code_generator.convert_end_if(is_empty)

    @property
    def _args_on_stack(self) -> int:
        return 0

    @property
    def _body(self) -> str | None:
        return None
