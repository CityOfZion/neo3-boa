from abc import ABC
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.identifiedsymbol import IdentifiedSymbol
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.bytestype import BytesType
from boa3.internal.model.variable import Variable


class ToIntMethod(IBuiltinMethod, ABC):
    def __init__(self, self_type: IType):
        identifier = 'to_int'
        if isinstance(self_type, IdentifiedSymbol):
            identifier = '-{0}_{1}'.format(self_type.identifier, identifier)

        args: dict[str, Variable] = {'self': Variable(self_type)}
        from boa3.internal.model.type.type import Type
        super().__init__(identifier, args, return_type=Type.int)

    @property
    def _arg_self(self) -> Variable:
        return self.args['self']

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        return isinstance(params[0], IExpression) and isinstance(params[0].type, BytesType)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.type.type import Type
        code_generator.convert_cast(Type.int, is_internal=True)

    def push_self_first(self) -> bool:
        return self.has_self_argument

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return None


class _ConvertToIntMethod(ToIntMethod):
    def __init__(self):
        super().__init__(None)

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, BytesType):
            return BytesToIntMethod(value)
        # if it is not a valid type, show mismatched type with bytes
        return BytesToIntMethod()


ToInt = _ConvertToIntMethod()


class BytesToIntMethod(ToIntMethod):
    def __init__(self, self_type: IType = None):
        if not isinstance(self_type, BytesType):
            from boa3.internal.model.type.type import Type
            self_type = Type.bytes
        super().__init__(self_type)

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self.args['self'].type):
            return self
        if isinstance(value, BytesType):
            return BytesToIntMethod(value)
        return super().build(value)
