import ast
from typing import Any, Dict, List, Optional, Tuple, Union

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

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String
        range_error_msg = String('range() arg 3 must not be zero').to_bytes()
        return [
            (Opcode.PUSH2, b''),
            (Opcode.PICK, b''),
            (Opcode.SIGN, b''),
            (Opcode.JMPIF, Integer(5 + len(range_error_msg)).to_byte_array(signed=True)),
            (Opcode.PUSHDATA1, Integer(len(range_error_msg)).to_byte_array(signed=True) + range_error_msg),
            (Opcode.THROW, b''),
            (Opcode.NEWARRAY0, b''),
            (Opcode.REVERSE4, b''),
            (Opcode.SWAP, b''),
            (Opcode.JMP, Integer(8).to_byte_array(signed=True, min_length=1)),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.OVER, b''),
            (Opcode.APPEND, b''),
            (Opcode.OVER, b''),
            (Opcode.ADD, b''),
            (Opcode.DUP, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.PUSH3, b''),
            (Opcode.PICK, b''),
            (Opcode.SIGN, b''),
            (Opcode.PUSH0, b''),
            (Opcode.JMPGT, Integer(5).to_byte_array(signed=True, min_length=1)),
            (Opcode.GT, b''),
            (Opcode.JMP, Integer(3).to_byte_array(signed=True, min_length=1)),
            (Opcode.LT, b''),
            (Opcode.JMPIF, Integer(-19).to_byte_array(signed=True, min_length=1)),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b'')
        ]

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
