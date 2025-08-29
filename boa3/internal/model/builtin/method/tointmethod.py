import ast
from typing import Any

from boa3.internal.model import set_internal_call
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.variable import Variable
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ToIntMethod(IBuiltinMethod):
    def __init__(self):
        identifier = 'to_int'

        args: dict[str, Variable] = {
            'value': Variable(Type.bytes),
            'big_endian': Variable(Type.bool),
            'signed': Variable(Type.bool),
        }
        big_endian_default = set_internal_call(ast.parse("{0}".format(True)
                                                            ).body[0].value)
        signed_default = set_internal_call(ast.parse("{0}".format(Type.bool.default_value)
                                                     ).body[0].value)

        super().__init__(identifier, args, defaults=[big_endian_default, signed_default],
                         return_type=Type.int)

    @property
    def generation_order(self) -> list[int]:
        value_index = list(self.args).index('value')
        big_endian_index = list(self.args).index('big_endian')
        signed_index = list(self.args).index('signed')

        return [signed_index, value_index, big_endian_index]

    def generate_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        # stack: signed, value, big_endian

        # if big_endian:
        if_is_big_endian = code_generator.convert_begin_if()
        #   value = value[::-1]
        code_generator.convert_array_negative_stride()

        code_generator.convert_end_if(if_is_big_endian, is_internal=True)
        # stack: signed, value

        code_generator.swap_reverse_stack_items(2)
        # if signed:
        if_is_signed = code_generator.convert_begin_if()

        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_literal(0b10000000)
        code_generator.convert_operation(BinaryOp.BitAnd)

        if_last_byte_not_begins_with_1 = code_generator.convert_begin_if()
        code_generator.change_jump(if_last_byte_not_begins_with_1, Opcode.JMPIF)

        else_is_not_signed = code_generator.convert_begin_else(if_is_signed, is_internal=True)
        #  value = value + b'\x00'
        code_generator.convert_literal(b'\x00')
        code_generator.convert_operation(BinaryOp.Concat)

        code_generator.convert_end_if(if_last_byte_not_begins_with_1, is_internal=True)
        code_generator.convert_end_if(else_is_not_signed, is_internal=True)
        # stack: value

        self.generate_internal_opcodes(code_generator)

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_cast(Type.int, is_internal=True)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['value'].type):
            return self
        if isinstance(value, BytesType):
            return ToIntMethod()
        return super().build(value)


ToInt = ToIntMethod()
