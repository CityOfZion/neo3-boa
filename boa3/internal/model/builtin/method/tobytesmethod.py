import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.primitive.strtype import StrType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.model.type.type import Type


class ToBytesMethod(IBuiltinMethod):
    def __init__(self, args: dict[str, Variable] = None, defaults: list[ast.AST] = None):
        identifier = 'to_bytes'
        super().__init__(identifier, args, defaults=defaults, return_type=Type.bytes)

    @property
    def _arg_value(self) -> Variable:
        return self.args['value']

    @property
    def identifier(self) -> str:
        if isinstance(self._arg_value.type, IdentifiedSymbol):
            return '-{0}_{1}'.format(self._arg_value.type.identifier, self._identifier)
        return self._identifier

    def generate_internal_opcodes(self, code_generator):
        code_generator.convert_cast(Type.bytes, is_internal=True)

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        if Type.int.is_type_of(value[0]):
            return IntToBytesMethod(value[0])
        elif Type.str.is_type_of(value[0]):
            return StrToBytesMethod(value[0])
        # if it is not a valid type, show mismatched type with int
        return IntToBytesMethod()

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class IntToBytesMethod(ToBytesMethod):
    def __init__(self, value_type: IType = None):
        if not isinstance(value_type, IntType):
            value_type = Type.int

        args: dict[str, Variable] = {
            'value': Variable(value_type),
            'length': Variable(Type.int),
            'big_endian': Variable(Type.bool),
            'signed': Variable(Type.bool)
        }

        length_default = ast.parse("{0}".format(1)
                                   ).body[0].value
        big_endian_default = ast.parse("{0}".format(True)
                                       ).body[0].value
        signed_default = ast.parse("{0}".format(Type.bool.default_value)
                                   ).body[0].value

        super().__init__(args, [length_default, big_endian_default, signed_default])

    @property
    def generation_order(self) -> list[int]:
        value_index = list(self.args).index('value')
        length_index = list(self.args).index('length')
        big_endian_index = list(self.args).index('big_endian')
        signed_index = list(self.args).index('signed')

        return [big_endian_index, signed_index, length_index, value_index]

    @property
    def exception_message(self) -> str:
        return 'can not convert int to bytes'

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        padding_positive = b'\x00'
        padding_negative = b'\xFF'
        forgot_signed_arg_message = ', did you call to_bytes on a negative integer without setting signed=True?'
        length_arg_too_small_message = ', try raising the value of the length argument'

        # stack: big_endian, signed, length, value

        code_generator.duplicate_stack_top_item()
        # if value == 0: value_bytes = b'\x00' * length
        if_int_is_zero = code_generator.convert_begin_if()
        code_generator.change_jump(if_int_is_zero, Opcode.JMPIF)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.convert_literal(padding_positive)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.StrBytesMul)

        # else:
        else_int_is_not_zero = code_generator.convert_begin_else(if_int_is_zero, is_internal=True)
        #   convert value to bytes (e.g., 4660 -> b'\x12\x34')
        super().generate_internal_opcodes(code_generator)

        code_generator.swap_reverse_stack_items(2)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        # stack: big_endian, value_bytes, length, signed

        # if not signed:
        if_not_signed = code_generator.convert_begin_if()
        code_generator.change_jump(if_not_signed, Opcode.JMPIF)

        #   if value < 0: raise Exception
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + forgot_signed_arg_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

        #   last_bytes_value = value_bytes[-1]
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_literal(padding_positive)

        #   if last_bytes_value == 0x00: value_bytes = value_bytes[:-1]
        if_starts_with_0x00 = code_generator.convert_begin_if()
        code_generator.change_jump(if_starts_with_0x00, Opcode.JMPNE)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_literal(0)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.swap_reverse_stack_items(2)

        code_generator.convert_end_if(if_starts_with_0x00)
        # stack: big_endian, value_bytes, length
        # else if signed:
        else_if_is_signed = code_generator.convert_begin_else(if_not_signed)

        #   if value < 0: padding = b'\xFF'
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        if_value_negative = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_negative, Opcode.JMPGE)
        code_generator.convert_literal(padding_negative)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        #   else if value >= 0:
        else_is_positive = code_generator.convert_begin_else(if_value_negative, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        #       first_bytes_value = value_bytes[0]
        code_generator.convert_literal(0b10000000)
        code_generator.convert_operation(BinaryOp.BitAnd)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(3)
        code_generator.convert_operation(BinaryOp.Eq)
        code_generator.convert_operation(BinaryOp.And)

        #       if first_bytes_value & 0b10000000 != 0 and len(value_bytes) == length: raise Exception
        if_positive_value_is_too_big = code_generator.convert_begin_if()
        code_generator.convert_literal(self.exception_message + length_arg_too_small_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_positive_value_is_too_big, is_internal=True)

        # stack: big_endian, value_bytes, length
        code_generator.convert_end_if(else_if_is_signed, is_internal=True)
        # padding = b'\x00' when positive
        code_generator.convert_literal(padding_positive)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        # stack: big_endian, padding, value_bytes, length

        code_generator.convert_end_if(else_is_positive, is_internal=True)

        # amount_of_zeros = length - len(value)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Sub)

        # if amount_of_zeros < 0: raise Exception
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + length_arg_too_small_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

        # zero_bytes = amount_of_zeros * padding_positive
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.StrBytesMul)
        code_generator.swap_reverse_stack_items(3)

        # if big_endian:
        if_is_big_endian = code_generator.convert_begin_if()
        #   result = value_bytes[::-1] (e.g., b'\x12\x34' -> b'\x34\x12')
        code_generator.convert_array_negative_stride()
        #   result = zero_bytes + result

        # else: # is little endian
        else_is_little_endian = code_generator.convert_begin_else(if_is_big_endian, is_internal=True)
        #   result = value_bytes + zero_bytes
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_end_if(else_is_little_endian, is_internal=True)

        code_generator.convert_operation(BinaryOp.Concat)

        code_generator.convert_end_if(else_int_is_not_zero, is_internal=True)


class StrToBytesMethod(ToBytesMethod):
    def __init__(self, value_type: IType = None):
        if not isinstance(value_type, StrType):
            value_type = Type.str

        args: dict[str, Variable] = {
            'value': Variable(value_type),
        }

        super().__init__(args)

    def generate_internal_opcodes(self, code_generator):
        # string and bytes' stack item are the same
        pass
