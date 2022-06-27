from abc import ABC
from typing import Any, Dict, List, Optional, Sequence, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.identifiedsymbol import IdentifiedSymbol
from boa3.model.type.itype import IType
from boa3.model.type.primitive.bytestringtype import ByteStringType
from boa3.model.type.primitive.bytestype import BytesType
from boa3.model.type.primitive.inttype import IntType
from boa3.model.type.primitive.strtype import StrType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ToBytesMethod(IBuiltinMethod, ABC):
    def __init__(self, self_type: IType):
        identifier = 'to_bytes'
        if isinstance(self_type, IdentifiedSymbol):
            identifier = '-{0}_{1}'.format(self_type.identifier, identifier)

        args: Dict[str, Variable] = {'self': Variable(self_type)}
        from boa3.model.type.type import Type
        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, BytesType)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.type.type import Type
        return [
            (Opcode.CONVERT, Type.bytes.stack_item)
        ]

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None


class _ConvertToBytesMethod(ToBytesMethod):
    def __init__(self):
        super().__init__(None)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, IntType):
            return IntToBytesMethod(value)
        elif isinstance(value, (StrType, ByteStringType)):
            return StrToBytesMethod(value)
        # if it is not a valid type, show mismatched type with int
        return IntToBytesMethod()


ToBytes = _ConvertToBytesMethod()


class IntToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        if not isinstance(self_type, IntType):
            from boa3.model.type.type import Type
            self_type = Type.int
        super().__init__(self_type)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sequence) and len(value) == 1:
            value = value[0]
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, IntType):
            return IntToBytesMethod(value)
        return super().build(value)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.compiler.codegenerator import get_bytes_count
        from boa3.neo.vm.type.Integer import Integer

        number_zero_to_bytes = b'\x00'
        jmp_place_holder = (Opcode.JMP, b'\x01')

        verify_number_is_zero = [
            (Opcode.DUP, b''),
            (Opcode.NZ, b''),
            jmp_place_holder
        ]

        number_is_not_zero = super().opcode.copy()
        number_is_not_zero.append(jmp_place_holder)

        number_is_zero = [
            (Opcode.DROP, b''),
            (Opcode.PUSHDATA1, Integer(len(number_zero_to_bytes)).to_byte_array() + number_zero_to_bytes),
        ]

        number_is_not_zero[-1] = Opcode.get_jump_and_data(Opcode.JMP, get_bytes_count(number_is_zero))

        verify_number_is_zero[-1] = Opcode.get_jump_and_data(Opcode.JMPIFNOT, get_bytes_count(number_is_not_zero))

        return (
            verify_number_is_zero +
            number_is_not_zero +
            number_is_zero
        )


class StrToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        if not isinstance(self_type, (StrType, ByteStringType)):
            from boa3.model.type.type import Type
            self_type = Type.str
        super().__init__(self_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        # string and bytes' stack item are the same
        return []

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sequence) and len(value) == 1:
            value = value[0]
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, StrType):
            return StrToBytesMethod(value)
        return super().build(value)
