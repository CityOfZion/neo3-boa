import ast
from typing import Any, Dict, List, Optional, Union

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class RangeMethod(IBuiltinMethod):

    def __init__(self, values_types: List[IType] = None):
        from boa3.internal.model.type.type import Type
        identifier = 'range'
        if not isinstance(values_types, list) or len(values_types) < 1:
            stop = Variable(Type.none)
            start = Variable(Type.none)
            step = Variable(Type.none)
        else:
            stop = Variable(Type.int)
            start = Variable(Type.int)
            step = Variable(Type.int)

        args: Dict[str, Variable] = {
            'stop': stop,
            'start': start,
            'step': step
        }
        start_default = ast.parse("{0}".format(Type.int.default_value)
                                  ).body[0].value
        step_default = ast.parse("1").body[0].value
        super().__init__(identifier, args, defaults=[start_default, step_default], return_type=Type.range)

    @property
    def _arg_stop(self) -> Variable:
        return self.args['stop']

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
        if self._arg_stop.type is Type.none:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self._arg_stop.type._identifier)

    @property
    def requires_reordering(self) -> bool:
        return True

    def reorder(self, arguments: list):
        if len(arguments) > 1:
            # swap start and stop default positions
            arguments[0], arguments[1] = arguments[1], arguments[0]

    def validate_parameters(self, *params: Union[IExpression, IType]) -> bool:
        if len(params) < 1 or len(params) > 3:
            return False

        if any(not isinstance(param, (IExpression, IType)) for param in params):
            return False

        params_type: List[IType] = [param if isinstance(param, IType) else param.type for param in params]
        from boa3.internal.model.type.type import Type
        return all(param is Type.int for param in params_type)

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.operation.binaryop import BinaryOp

        range_error_msg = 'range() arg 3 must not be zero'

        code_generator.duplicate_stack_item(3)
        code_generator.insert_opcode(Opcode.SIGN)
        # if step == 0
        if_invalid_step = code_generator.convert_begin_if()
        code_generator.change_jump(if_invalid_step, Opcode.JMPIF)
        #   raise error
        code_generator.convert_literal(range_error_msg)
        code_generator.convert_raise_exception()

        code_generator.convert_end_if(if_invalid_step, is_internal=True)

        # aux = []
        code_generator.convert_literal([])
        # new_item = start
        code_generator.swap_reverse_stack_items(4)
        code_generator.swap_reverse_stack_items(2)

        # while new_item is valid
        begin_while = code_generator.convert_begin_while()

        #   aux.append(new_item)
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(2)
        code_generator.convert_builtin_method_call(Builtin.SequenceAppend, is_internal=True)
        #   new_item += step
        code_generator.duplicate_stack_item(2)
        code_generator.convert_operation(BinaryOp.Add, is_internal=True)

        # while condition
        test_while = code_generator.bytecode_size
        code_generator.duplicate_stack_top_item()
        code_generator.duplicate_stack_item(4)
        code_generator.duplicate_stack_item(4)
        code_generator.insert_opcode(Opcode.SIGN)
        code_generator.convert_literal(0)

        # if step <= 0 -> condition is GT
        if_condition = code_generator.convert_begin_if()
        code_generator.change_jump(if_condition, Opcode.JMPGT)  # jmp to negation of LE
        code_generator.convert_operation(BinaryOp.Gt, is_internal=True)

        # else -> condition is LT
        else_condition = code_generator.convert_begin_else(if_condition, is_internal=True)
        code_generator.convert_operation(BinaryOp.Lt, is_internal=True)
        code_generator.convert_end_if(else_condition, is_internal=True)

        code_generator.convert_end_while(begin_while, test_while, is_internal=True)

        # clear stack
        for _ in self.args:
            code_generator.remove_stack_top_item()

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if isinstance(value, list) and self.validate_parameters(*value):
            return RangeMethod(value)
        return super().build(value)
