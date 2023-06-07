from abc import ABC
from typing import Any, Dict, Optional, Sequence

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.type.primitive.inttype import IntType
from boa3.internal.model.type.primitive.strtype import StrType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ToBytesMethod(IBuiltinMethod, ABC):
    def __init__(self, self_type: IType):
        identifier = 'to_bytes'
        args: Dict[str, Variable] = {'self': Variable(self_type)}
        from boa3.internal.model.type.type import Type
        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, BytesType)

    @property
    def identifier(self) -> str:
        if isinstance(self._arg_self.type, IdentifiedSymbol):
            return '-{0}_{1}'.format(self._arg_self.type.identifier, self._identifier)
        return self._identifier

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type
        code_generator.convert_cast(Type.bytes, is_internal=True)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, IntType):
            return IntToBytesMethod(value)
        elif isinstance(value, StrType):
            return StrToBytesMethod(value)
        # if it is not a valid type, show mismatched type with int
        return IntToBytesMethod()

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


ToBytes = _ConvertToBytesMethod()


class IntToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        if not isinstance(self_type, IntType):
            from boa3.internal.model.type.type import Type
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

    def generate_internal_opcodes(self, code_generator):
        code_generator.duplicate_stack_top_item()
        code_generator.insert_opcode(Opcode.NZ)
        is_zero = code_generator.convert_begin_if()
        # if number != 0:
        #   generic implementation
        super().generate_internal_opcodes(code_generator)
        # else:
        is_zero = code_generator.convert_begin_else(is_zero, is_internal=True)
        #   result = b'\x00'
        code_generator.remove_stack_top_item()
        code_generator.convert_literal(b'\x00')

        code_generator.convert_end_if(is_zero, is_internal=True)


class StrToBytesMethod(ToBytesMethod):
    def __init__(self, self_type: IType = None):
        if not isinstance(self_type, StrType):
            from boa3.internal.model.type.type import Type
            self_type = Type.str
        super().__init__(self_type)

    def generate_internal_opcodes(self, code_generator):
        # string and bytes' stack item are the same
        pass

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, Sequence) and len(value) == 1:
            value = value[0]
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, StrType):
            return StrToBytesMethod(value)
        return super().build(value)
