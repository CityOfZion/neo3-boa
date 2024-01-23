import ast
from typing import Any

from boa3.internal import constants
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class UInt160Method(IBuiltinMethod):

    def __init__(self, return_type: UInt160Type, argument_type: IType = None):
        from boa3.internal.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.none

        identifier = 'UInt160'
        args: dict[str, Variable] = {'object': Variable(argument_type)}

        args_default = ast.parse("{0}".format(Type.int.default_value)
                                 ).body[0].value

        super().__init__(identifier, args, [args_default], return_type=return_type)

    @property
    def _arg_object(self) -> Variable:
        return self.args['object']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_object.type is Type.none:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_object.type._identifier)

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

        return (Type.bytes.is_type_of(param_type)
                or Type.int.is_type_of(param_type))

    def evaluate_literal(self, *args: Any) -> Any:
        from boa3.internal.neo3.core.types import UInt160

        if len(args) == 0:
            return UInt160.zero().to_array()

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, int):
                from boa3.internal.neo.vm.type.Integer import Integer
                arg = Integer(arg).to_byte_array(min_length=UInt160._BYTE_LEN)
            if isinstance(arg, bytes):
                value = UInt160(arg).to_array()
                return value

        return super().evaluate_literal(*args)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp
        from boa3.internal.model.type.type import Type

        code_generator.duplicate_stack_top_item()
        code_generator.insert_type_check(Type.int.stack_item)
        # if isinstance(arg, int):
        is_int = code_generator.convert_begin_if()

        #   assert num >= 0
        code_generator.duplicate_stack_top_item()
        code_generator.convert_literal(0)
        code_generator.convert_operation(BinaryOp.GtE, is_internal=True)
        code_generator.convert_assert()

        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(constants.SIZE_OF_INT160)
        code_generator.duplicate_stack_item(2)
        code_generator.duplicate_stack_item(2)

        #   if len(num) < 20
        need_to_adjust_size = code_generator.convert_begin_if()
        code_generator.change_jump(need_to_adjust_size, Opcode.JMPGE)

        #       # increase length of number to 20
        code_generator.convert_literal(bytes(constants.SIZE_OF_INT160))
        code_generator.swap_reverse_stack_items(3)
        code_generator.convert_operation(BinaryOp.Sub, is_internal=True)
        code_generator.insert_opcode(Opcode.LEFT, pop_from_stack=True, add_to_stack=[Type.bytes])
        code_generator.convert_operation(BinaryOp.Concat.build(Type.bytes, Type.bytes), is_internal=True)

        #   else:
        need_to_adjust_size = code_generator.convert_begin_else(need_to_adjust_size, is_internal=True)
        #       # clean stack
        code_generator.remove_stack_top_item()
        code_generator.remove_stack_top_item()

        code_generator.convert_end_if(need_to_adjust_size, is_internal=True)
        code_generator.convert_end_if(is_int, is_internal=True)

        #   # convert to uint160
        code_generator.convert_cast(self.return_type, is_internal=True)

        # assert len(value) == 20
        code_generator.duplicate_stack_top_item()
        code_generator.convert_builtin_method_call(Builtin.Len, is_internal=True)
        code_generator.convert_literal(constants.SIZE_OF_INT160)
        code_generator.convert_operation(BinaryOp.NumEq, is_internal=True)
        code_generator.convert_assert()

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> str | None:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_object.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return UInt160Method(self.return_type, value)
        return super().build(value)
