import ast
from typing import Any

from boa3.internal.compiler.codegenerator.generatordata import GeneratorData
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
            'length': Variable(Type.optional.build(Type.int)),
            'big_endian': Variable(Type.bool),
            'signed': Variable(Type.bool)
        }

        length_default = ast.parse("{0}".format(None)
                                   ).body[0].value
        big_endian_default = ast.parse("{0}".format(False)
                                       ).body[0].value
        signed_default = ast.parse("{0}".format(True)
                                   ).body[0].value

        super().__init__(args, [length_default, big_endian_default, signed_default])

        self.padding_negative = b'\xFF'
        self.padding_positive = b'\x00'
        self.length_arg_too_small_message = ', try raising the value of the length argument'
        self.forgot_signed_arg_message = ', did you call to_bytes on a negative integer without setting signed=True?'

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

    @property
    def warning_message(self) -> str | None:
        if len(self.runtime_args) > 1 or len(self.runtime_kwargs) > 0:
            return None

        return ("Neo3-boa uses little-endian and signed representation by default, "
                "it also automatically calculates the length. "
                "See the method documentation for more details.")

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.operation.binaryop import BinaryOp

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

        is_const_length, const_length = get_constant(self.runtime_args_generated[2])
        is_const_big_endian, const_big_endian = get_constant(self.runtime_args_generated[0])
        is_const_signed, const_signed = get_constant(self.runtime_args_generated[1])

        # stack: big_endian, signed, length, value

        if not is_const_length:
            code_generator.duplicate_stack_item(2)
            code_generator.convert_literal(None)
            code_generator.convert_operation(BinaryOp.Is)
            # if length is None:
            if_len_is_null = code_generator.convert_begin_if()
            code_generator.change_jump(if_len_is_null, Opcode.JMPIFNOT)
            self.opcode_length_none(code_generator)
            code_generator.convert_end_if(if_len_is_null)
        elif is_const_length and const_length is None:
            self.opcode_length_none(code_generator)

        # stack: big_endian, signed, length, value

        code_generator.duplicate_stack_top_item()
        # if value == 0: value_bytes = b'\x00' * length
        if_int_is_zero = code_generator.convert_begin_if()
        code_generator.change_jump(if_int_is_zero, Opcode.JMPIF)
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_item(2)
        code_generator.remove_stack_item(2)
        code_generator.convert_literal(self.padding_positive)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.StrBytesMul)

        # else:
        else_int_is_not_zero = code_generator.convert_begin_else(if_int_is_zero, is_internal=True)
        #   convert value to bytes (e.g., 4660 -> b'\x12\x34')
        super().generate_internal_opcodes(code_generator)

        code_generator.swap_reverse_stack_items(2)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        # stack: big_endian, value_bytes, length, signed

        if not is_const_signed:
            # if not signed:
            if_not_signed = code_generator.convert_begin_if()
            code_generator.change_jump(if_not_signed, Opcode.JMPIF)
            self.opcode_signed_false(code_generator)

            # else if signed:
            else_if_is_signed = code_generator.convert_begin_else(if_not_signed)
            self.opcode_signed_true(code_generator)
            code_generator.convert_end_if(else_if_is_signed, is_internal=True)
        elif is_const_signed:
            code_generator.remove_stack_top_item()
            if const_signed:
                self.opcode_signed_true(code_generator)
            else:
                self.opcode_signed_false(code_generator)

        # stack: big_endian, padding, value_bytes, length

        # amount_of_zeros = length - len(value)
        code_generator.duplicate_stack_item(2)
        from boa3.internal.model.builtin.builtin import Builtin
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Sub)

        if not is_const_length or (is_const_length and const_length is not None):
            self.opcode_check_len_fits(code_generator)

        # zero_bytes = amount_of_zeros * padding
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.StrBytesMul)
        code_generator.swap_reverse_stack_items(3)

        if not is_const_big_endian:
            # if big_endian:
            if_is_big_endian = code_generator.convert_begin_if()
            self.opcode_big_endian_true(code_generator)
            #   result = zero_bytes + result

            # else: # is little endian
            else_is_little_endian = code_generator.convert_begin_else(if_is_big_endian, is_internal=True)
            self.opcode_big_endian_false(code_generator)
            #   result = value_bytes + zero_bytes
            code_generator.convert_end_if(else_is_little_endian, is_internal=True)
        elif is_const_big_endian:
            code_generator.remove_stack_top_item()
            if const_big_endian:
                self.opcode_big_endian_true(code_generator)
            else:
                self.opcode_big_endian_false(code_generator)

        code_generator.convert_operation(BinaryOp.Concat)

        code_generator.convert_end_if(else_int_is_not_zero, is_internal=True)

    def opcode_length_none(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        # stack: big_endian, signed, length, value

        code_generator.swap_reverse_stack_items(2)
        code_generator.remove_stack_top_item()
        code_generator.duplicate_stack_top_item()
        super().generate_internal_opcodes(code_generator)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        #   length = len(value)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)

        #     if length == 0: length = 1
        if_len_is_null_and_value_0 = code_generator.convert_begin_if()
        code_generator.change_jump(if_len_is_null_and_value_0, Opcode.JMPNE)
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(1)
        code_generator.convert_end_if(if_len_is_null_and_value_0)
        code_generator.swap_reverse_stack_items(2)

    def opcode_signed_false(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        # stack: big_endian, value_bytes, length, signed

        #   if value < 0: raise Exception
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + self.forgot_signed_arg_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

        #   last_bytes_value = value_bytes[-1]
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.insert_opcode(Opcode.DEC)
        code_generator.convert_literal(1)
        code_generator.convert_get_substring(is_internal=True)
        code_generator.convert_literal(self.padding_positive)

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

        # padding = b'\x00' when positive
        code_generator.convert_literal(self.padding_positive)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

    def opcode_signed_true(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        # stack: big_endian, value_bytes, length, signed

        #   if value < 0: padding = b'\xFF'
        code_generator.duplicate_stack_item(2)
        code_generator.convert_literal(0)
        if_value_negative = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_negative, Opcode.JMPGE)
        code_generator.convert_literal(self.padding_negative)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        #   else if value >= 0:
        else_is_positive = code_generator.convert_begin_else(if_value_negative, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Gt)

        #       if len(value_bytes) > length: raise Exception
        if_positive_value_is_too_big = code_generator.convert_begin_if()
        code_generator.convert_literal(self.exception_message + self.length_arg_too_small_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_positive_value_is_too_big, is_internal=True)
        # stack: big_endian, value_bytes, length

        # padding = b'\x00' when positive
        code_generator.convert_literal(self.padding_positive)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.swap_reverse_stack_items(3, rotate=True)
        code_generator.convert_end_if(else_is_positive, is_internal=True)

    def opcode_check_len_fits(self, code_generator):
        # stack: big_endian, padding, value_bytes, length

        # if amount_of_zeros < 0: raise Exception
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + self.length_arg_too_small_message)
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

    def opcode_big_endian_true(self, code_generator):
        #   result = value_bytes[::-1] (e.g., b'\x12\x34' -> b'\x34\x12')
        code_generator.convert_array_negative_stride()

    def opcode_big_endian_false(self, code_generator):
        code_generator.swap_reverse_stack_items(2)


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
