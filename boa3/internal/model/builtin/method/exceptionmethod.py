import ast
from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.variable import Variable


class ExceptionMethod(IBuiltinMethod):

    def __init__(self, argument_type: IType = None):
        from boa3.internal.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.str

        identifier = '-Exception'
        args: dict[str, Variable] = {'message': Variable(argument_type)}
        default_message = "'{0}'".format(self.default_message) if argument_type is Type.str else "{0}"
        default = ast.parse(default_message.format(argument_type.default_value)
                            ).body[0].value
        super().__init__(identifier, args, [default], return_type=Type.exception)

    @property
    def _arg_message(self) -> Variable:
        return self.args['message']

    @property
    def default_message(self) -> str:
        return 'usererror'

    @property
    def identifier(self) -> str:
        return self._identifier

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) > 1:
            return False
        if len(params) == 0:
            return True

        from boa3.internal.model.type.itype import IType
        if not isinstance(params[0], (IExpression, IType)):
            return False

        param_type: IType = params[0].type if isinstance(params[0], IExpression) else params[0]
        return isinstance(param_type, PrimitiveType)

    def generate_internal_opcodes(self, code_generator):
        pass

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_message.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return ExceptionMethod(value)
        return super().build(value)
