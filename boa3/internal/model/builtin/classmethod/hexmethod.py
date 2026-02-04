import ast

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.builtin.native.nativecontract import NativeContract
from boa3.internal.model.operation.binaryop import BinaryOp
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class HexMethod(IBuiltinMethod):
    sep_error_msg = "sep must be length 1"

    def __init__(self):
        identifier = 'hex'
        args: dict[str, Variable] = {
            'self': Variable(Type.bytes),
            'sep': Variable(Type.optional.build(Type.str)),
            'bytes_per_sep': Variable(Type.int),
        }

        sep_default = ast.parse("{0}".format(Type.none.default_value)
                                ).body[0].value
        bytes_per_sep_default = ast.parse("{0}".format(1)
                                          ).body[0].value

        super().__init__(identifier, args, defaults=[sep_default, bytes_per_sep_default], return_type=Type.str)

    def _arg_self(self) -> Variable:
        return self.args['self']

    def push_self_first(self) -> bool:
        return self.has_self_argument

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin

        """
        str_value = bytes_value.hex()

        if sep is not None:
            assert len(sep) == 1, sep_error_msg
                
            if bytes_per_sep != 0:
                index = len(string)
                mod_expected_value = 0 if bytes_per_sep < 0 else len(string) % bytes_per_sep
                
                index -= 2
                while index >= 2:
                    if ((index / 2) % bytes_per_sep) == mod_expected_value:    
                        str_value = str_value[:index] + sep + str_value[index:]
                    index -= 2
        """
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.convert_builtin_method_call(NativeContract.StdLib.class_methods['hex_encode'])

        # stack: bytes_per_sep, sep, str_value
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(None)
        code_generator.convert_operation(BinaryOp.Is)
        if_sep_not_none = code_generator.convert_begin_if()
        code_generator.change_jump(if_sep_not_none, Opcode.JMPIF)

        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(1)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        code_generator.convert_literal(self.sep_error_msg)
        code_generator.convert_assert(has_message=True)

        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(0)

        # if bytes_per_sep != 0:
        if_bytes_per_sep_not_zero = code_generator.convert_begin_if()
        code_generator.change_jump(if_bytes_per_sep_not_zero, Opcode.JMPEQ)

        #   assert len(sep) == 1, sep_error_msg
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(1)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        code_generator.convert_literal(self.sep_error_msg)
        code_generator.convert_assert(has_message=True)

        #   index = len(string)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        #   mod_expected_value = 0 if bytes_per_sep < 0 else len(string) % bytes_per_sep
        code_generator.duplicate_stack_item(4)
        code_generator.convert_literal(0)
        if_bytes_per_sep_negative = code_generator.convert_begin_if()
        code_generator.change_jump(if_bytes_per_sep_negative, Opcode.JMPGT)
        code_generator.convert_literal(0)
        else_bytes_per_sep_pos = code_generator.convert_begin_else(if_bytes_per_sep_negative)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(2)
        code_generator.convert_operation(BinaryOp.IntDiv, is_internal=True)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Mod, is_internal=True)
        code_generator.convert_end_if(else_bytes_per_sep_pos, is_internal=True)

        # stack: bytes_per_sep, sep, str_value, index, mod_expected_value
        #   while index >= 2:
        start_loop = code_generator.convert_begin_while()

        #       if ((index / 2) % bytes_per_sep) == mod_expected_value:
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(2)
        code_generator.convert_operation(BinaryOp.IntDiv, is_internal=True)
        code_generator.duplicate_stack_item(6)
        code_generator.convert_operation(BinaryOp.Mod, is_internal=True)
        code_generator.duplicate_stack_item(2)
        if_should_add_separator = code_generator.convert_begin_if()
        code_generator.change_jump(if_should_add_separator, Opcode.JMPNE)

        #           str_value = str_value[:index] + sep + str_value[index:]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.insert_opcode(Opcode.LEFT, pop_from_stack=True, add_to_stack=[Type.str])
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.move_stack_item_to_top(4)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.RIGHT, pop_from_stack=True, add_to_stack=[Type.str])
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        code_generator.convert_end_if(if_should_add_separator, is_internal=True)

        # while condition:
        start_loop_condition = code_generator.bytecode_size
        #   index -= 2
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(2)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)

        code_generator.convert_end_while(start_loop, start_loop_condition, is_internal=True)

        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()
        code_generator.convert_cast(Type.str, is_internal=True)

        code_generator.convert_end_if(if_bytes_per_sep_not_zero, is_internal=True)
        code_generator.convert_end_if(if_sep_not_none, is_internal=True)

        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
