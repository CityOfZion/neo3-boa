import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.primitive.strtype import StrType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ToBytesMethod(IBuiltinMethod):
    def __init__(self, args: dict[str, Variable] = None, defaults: list[ast.AST] = None):
        identifier = 'to_bytes'
        from boa3.internal.model.type.type import Type
        super().__init__(identifier, args, defaults=defaults, return_type=Type.bytes)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    @property
    def identifier(self) -> str:
        if isinstance(self._arg_self.type, IdentifiedSymbol):
            return '-{0}_{1}'.format(self._arg_self.type.identifier, self._identifier)
        return self._identifier

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type
        code_generator.convert_cast(Type.bytes, is_internal=True)

    def build(self, value: Any) -> IBuiltinMethod:
        if not isinstance(value, list):
            value = [value]

        from boa3.internal.model.type.type import Type

        if Type.int.is_type_of(value[0]):
            return IntToBytesMethod(value[0])
        elif Type.str.is_type_of(value[0]):
            return StrToBytesMethod(value[0])
        # if it is not a valid type, show mismatched type with int
        return IntToBytesMethod()

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class IntToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, IntType):
            self_type = Type.int

        args: dict[str, Variable] = {
            'self': Variable(self_type),
            'length': Variable(Type.int),
            'big_endian': Variable(Type.bool)
        }

        length_default = ast.parse("{0}".format(1)
                                   ).body[0].value
        big_endian_default = ast.parse("{0}".format(True)
                                       ).body[0].value

        super().__init__(args, [length_default, big_endian_default])

    @property
    def generation_order(self) -> list[int]:
        self_index = list(self.args).index('self')
        length_index = list(self.args).index('length')
        big_endian_index = list(self.args).index('big_endian')

        return [big_endian_index, self_index, length_index]

    @property
    def exception_message(self) -> str:
        return 'can not convert int to bytes'

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        # big_endian, self, length

        # amount_of_zeros = length - len(self)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_operation(BinaryOp.Sub)

        # if amount_of_zeros < 0: raise Exception
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + ', length is too small')
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

        # zero_bytes = amount_of_zeros * b'\x00'
        code_generator.convert_literal(b'\x00')
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.StrBytesMul)

        # if self < 0: raise Exception
        code_generator.swap_reverse_stack_items(2)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        if_value_is_bigger_than_length = code_generator.convert_begin_if()
        code_generator.change_jump(if_value_is_bigger_than_length, Opcode.JMPGE)
        code_generator.convert_literal(self.exception_message + ', negative integers are not supported')
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(if_value_is_bigger_than_length, is_internal=True)

        # convert self to bytes (e.g., 4660 -> b'\x12\x34')
        super().generate_internal_opcodes(code_generator)
        code_generator.swap_reverse_stack_items(3, rotate=True)

        # if big_endian:
        if_is_big_endian = code_generator.convert_begin_if()
        #   result = self_bytes[::-1] (e.g., b'\x12\x34' -> b'\x34\x12')
        code_generator.convert_array_negative_stride()
        code_generator.swap_reverse_stack_items(2)

        #   result = zero_bytes + result
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat)

        # else: # is little endian
        else_is_little_endian = code_generator.convert_begin_else(if_is_big_endian, is_internal=True)
        #   result = self_bytes + zero_bytes
        code_generator.swap_reverse_stack_items(2)
        code_generator.convert_operation(BinaryOp.Concat)

        code_generator.convert_end_if(else_is_little_endian, is_internal=True)


class StrToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        from boa3.internal.model.type.type import Type

        if not isinstance(self_type, StrType):
            self_type = Type.str

        args: dict[str, Variable] = {
            'self': Variable(self_type),
        }

        super().__init__(args)

    def generate_internal_opcodes(self, code_generator):
        # string and bytes' stack item are the same
        pass
