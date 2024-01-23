from typing import Any

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ECPointMethod(IBuiltinMethod):

    def __init__(self, return_type: ECPointType, argument_type: IType = None):
        from boa3.internal.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.none

        identifier = 'ECPoint'
        args: dict[str, Variable] = {'arg': Variable(argument_type)}

        super().__init__(identifier, args, return_type=return_type)

    @property
    def _arg_arg(self) -> Variable:
        return self.args['arg']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_arg.type is Type.none:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_arg.type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) > 1:
            return False
        if len(params) == 0:
            return True

        from boa3.internal.model.type.itype import IType
        if not isinstance(params[0], (IExpression, IType)):
            return False

        param_type: IType = params[0].type if isinstance(params[0], IExpression) else params[0]
        from boa3.internal.model.type.type import Type
        return Type.bytes.is_type_of(param_type)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal import constants
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.operation.unaryop import UnaryOp

        # if (arg is not None
        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(None)
        code_generator.convert_operation(UnaryOp.Not, is_internal=True)

        is_arg_null = code_generator.convert_begin_if()
        #       or len(arg) != ECPOINT_SIZE):
        code_generator.convert_cast(self.return_type, is_internal=True)
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(constants.SIZE_OF_ECPOINT)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)

        else_address = code_generator.convert_begin_else(is_arg_null, True)
        code_generator.change_jump(else_address, Opcode.JMPIF)
        #   raise exception
        code_generator.convert_raise_exception()
        code_generator.convert_end_if(else_address, is_internal=True)

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_arg.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return ECPointMethod(self.return_type, value)
        return super().build(value)
