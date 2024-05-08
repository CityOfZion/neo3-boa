from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.ibytestringtype import IByteStringType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class LowerMethod(IBuiltinMethod):
    def __init__(self, self_type: IByteStringType = None):
        if not isinstance(self_type, IByteStringType):
            from boa3.internal.model.type.type import Type
            self_type = Type.bytes

        identifier = 'lower'
        args: dict[str, Variable] = {'self': Variable(self_type)}

        super().__init__(identifier, args, return_type=self_type)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.neo.vm.type.Integer import Integer

        upper_a = Integer(ord('A')).to_byte_array()
        upper_z = Integer(ord('Z')).to_byte_array()

        # string = arg
        code_generator.duplicate_stack_top_item()
        # max_index = len(arg)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)

        # index = 0
        code_generator.convert_literal(0)

        # while index < max_index
        while_begin = code_generator.convert_begin_while()

        #   substr_left = string[:index]
        code_generator.swap_reverse_stack_items(3)
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_get_sequence_beginning()
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        #   modifier = 1, since using upper is only supported with ASCII for now
        code_generator.duplicate_stack_item(2)  # TODO: verify if string[index] < c0 when other values are implemented #2kq1ywb
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(1)

        #   substr_middle = string[index:index+modifier]
        code_generator.convert_get_substring(is_internal=True)

        #   if 'A' <= substr_middle <= 'Z':
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(upper_a)
        if_lower_than_a = code_generator.convert_begin_if()
        code_generator.change_jump(if_lower_than_a, Opcode.JMPLT)

        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(upper_z)
        if_greater_than_z = code_generator.convert_begin_if()
        code_generator.change_jump(if_greater_than_z, Opcode.JMPGT)

        #       substr_middle = lower(substr_middle)
        code_generator.convert_literal(ord('a') - ord('A'))
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)
        code_generator.convert_cast(self.type)

        code_generator.convert_end_if(if_greater_than_z)
        code_generator.convert_end_if(if_lower_than_a)

        #   substr_right = string[index+modifier:]
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.insert_opcode(Opcode.INC)
        code_generator.convert_get_sequence_ending()

        concat = BinaryOp.Concat.build(self.type, self.type)  # ensure the correct type on generator stack
        #   string = substr_left + substr_middle + substr_right
        code_generator.convert_operation(concat, is_internal=True)
        code_generator.convert_operation(concat)
        code_generator.remove_stack_item(2)
        code_generator.swap_reverse_stack_items(3)

        #   index += 1
        code_generator.insert_opcode(Opcode.INC)

        while_condition = code_generator.bytecode_size
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        code_generator.convert_end_while(while_begin, while_condition, is_internal=True)

        # clean stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, IByteStringType):
            return LowerMethod(value)
        return super().build(value)
