import ast
from typing import Any

from boa3.internal.compiler.codegenerator.generatordata import GeneratorData
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
        big_endian_default = set_internal_call(ast.parse("{0}".format(False)
                                                            ).body[0].value)
        signed_default = set_internal_call(ast.parse("{0}".format(True)
                                                     ).body[0].value)

        super().__init__(identifier, args, defaults=[big_endian_default, signed_default],
                         return_type=Type.int)

    @property
    def generation_order(self) -> list[int]:
        value_index = list(self.args).index('value')
        big_endian_index = list(self.args).index('big_endian')
        signed_index = list(self.args).index('signed')

        return [signed_index, value_index, big_endian_index]

    @property
    def warning_message(self) -> str | None:
        if len(self.runtime_args) > 1 or len(self.runtime_kwargs) > 0:
            return None

        return ("Neo3-boa uses little-endian and signed representation by default. "
                "See the method documentation for more details.")

    def generate_opcodes(self, code_generator):
        def get_constant(data: GeneratorData) -> tuple[bool, Any]:
            is_constant = False
            value = None

            if isinstance(data.node, ast.Constant):
                is_constant = True
                value = data.node.value
            elif (
                    data.symbol is not None and
                    isinstance(data.symbol, Variable) and
                    isinstance(data.symbol.origin, ast.Assign) and
                    isinstance(data.symbol.origin.value, ast.Constant)
            ):
                is_constant = True
                value = data.symbol.origin.value.value

            return is_constant, value

        is_const_big_endian, const_big_endian = get_constant(self.runtime_args_generated[2])
        is_const_signed, const_signed = get_constant(self.runtime_args_generated[0])

        # stack: signed, value, big_endian

        if not is_const_big_endian:
            # if big_endian:
            if_is_big_endian = code_generator.convert_begin_if()
            #   value = value[::-1]
            self.opcode_big_endian_true(code_generator)
            code_generator.convert_end_if(if_is_big_endian)
        else:
            code_generator.remove_stack_top_item()
            if const_big_endian:
                self.opcode_big_endian_true(code_generator)

        # stack: signed, value

        code_generator.swap_reverse_stack_items(2)

        if not is_const_signed:
            # if signed:
            if_is_signed = code_generator.convert_begin_if()
            self.opcode_signed_true(code_generator)
            else_is_not_signed = code_generator.convert_begin_else(if_is_signed, is_internal=True)
            self.opcode_signed_false(code_generator)
            code_generator.convert_end_if(else_is_not_signed, is_internal=True)
        else:
            code_generator.remove_stack_top_item()
            if const_signed:
                self.opcode_signed_true(code_generator)
            else:
                self.opcode_signed_false(code_generator)

        # stack: value
        self.generate_internal_opcodes(code_generator)

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_cast(Type.int, is_internal=True)

    def opcode_signed_false(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

        #  value = value + b'\x00'
        code_generator.convert_literal(b'\x00')
        code_generator.convert_operation(BinaryOp.Concat)

    def opcode_signed_true(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_cast(Type.bytes, is_internal=True)
        code_generator.convert_literal(0b10000000)
        code_generator.convert_operation(BinaryOp.BitAnd)

        if_last_byte_not_begins_with_1 = code_generator.convert_begin_if()
        code_generator.change_jump(if_last_byte_not_begins_with_1, Opcode.JMPIF)

        #  value = value + b'\x00'
        code_generator.convert_literal(b'\x00')
        code_generator.convert_operation(BinaryOp.Concat)
        code_generator.convert_end_if(if_last_byte_not_begins_with_1, is_internal=True)

    def opcode_big_endian_true(self, code_generator):
        code_generator.convert_array_negative_stride()

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
