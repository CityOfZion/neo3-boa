from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.builtin.native.nativecontract import NativeContract
from boa3.internal.model.operation.unaryop import UnaryOp
from boa3.internal.model.type.type import Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class FromHexMethod(IBuiltinMethod):
    whitespace_error_msg = "non-hexadecimal number found in fromhex() arg"

    def __init__(self):
        from boa3.internal.model.type.type import Type

        identifier = 'fromhex'
        args: dict[str, Variable] = {
            'string': Variable(Type.str),
        }

        super().__init__(identifier, args, return_type=Type.bytes)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # go over the string and check if there are any " " characters, if there are, replace them with ""
        """
        index = 0
        end = len(string)
        
        while index < end:
            if string[index] == ' ':
                assert index % 2 == 1, self.whitespace_error_msg
                string = string[:index] + string[index+1:]
                end -= 1
            else:
                index += 1    
        """
        # stack: string

        # index = 0; end = len(string)
        code_generator.convert_literal(0)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        # stack: string, index, end
        #         while index < end:
        start_loop = code_generator.convert_begin_while()
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True, fix_result_type=True)
        code_generator.convert_literal(' ')

        # if string[index] == ' ':
        if_is_space = code_generator.convert_begin_if()
        code_generator.change_jump(if_is_space, Opcode.JMPNE)

        #   assert index % 2 == 1, self.whitespace_error_msg
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(2)
        code_generator.convert_operation(BinaryOp.Mod, is_internal=True)
        code_generator.convert_operation(UnaryOp.Not, is_internal=True)
        code_generator.convert_literal(self.whitespace_error_msg)
        code_generator.convert_assert(has_message=True)

        #   string = string[:index] + string[index+1:]
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(3)
        code_generator.insert_opcode(Opcode.LEFT, pop_from_stack=True, add_to_stack=[Type.str])
        code_generator.move_stack_item_to_top(4)
        code_generator.duplicate_stack_item(3)
        code_generator.duplicate_stack_item(5)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.insert_opcode(Opcode.RIGHT, pop_from_stack=True, add_to_stack=[Type.str])
        code_generator.convert_operation(BinaryOp.Concat, is_internal=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        #   end -= 1
        code_generator.insert_opcode(Opcode.DEC)

        # else:
        #   index += 1
        else_is_not_space = code_generator.convert_begin_else(if_is_space, is_internal=True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_end_if(else_is_not_space, is_internal=True)

        # while condition:
        start_loop_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)

        code_generator.convert_end_while(start_loop, start_loop_condition, is_internal=True)

        # remove index and end
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        code_generator.convert_builtin_method_call(NativeContract.StdLib.class_methods['hex_decode'])

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None
