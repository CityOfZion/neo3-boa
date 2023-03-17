import ast
from typing import Any, Dict, List, Optional, Tuple

from boa3.internal import constants
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.uint256type import UInt256Type
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class UInt256Method(IBuiltinMethod):

    def __init__(self, return_type: UInt256Type, argument_type: IType = None):
        from boa3.internal.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.none

        identifier = 'UInt256'
        args: Dict[str, Variable] = {'object': Variable(argument_type)}

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
        from boa3.internal.neo3.core.types import UInt256

        if len(args) == 0:
            return UInt256.zero().to_array()

        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, int):
                from boa3.internal.neo.vm.type.Integer import Integer
                arg = Integer(arg).to_byte_array(min_length=UInt256._BYTE_LEN)
            if isinstance(arg, bytes):
                value = UInt256(arg).to_array()
                return value

        return super().evaluate_literal(*args)

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.model.type.type import Type

        from boa3.internal.neo.vm.type.StackItem import StackItemType
        return [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.int.stack_item),  # if istype(arg, int):
            (Opcode.JMPIFNOT, Integer(56).to_byte_array(signed=True)),
            (Opcode.DUP, b''),                       # assert num >= 0
            (Opcode.PUSH0, b''),
            (Opcode.GE, b''),
            (Opcode.ASSERT, b''),

            (Opcode.DUP, b''),                       # if len(num) < 32
            (Opcode.SIZE, b''),                        # increase number's length to 32
            (Opcode.PUSHINT8, Integer(constants.SIZE_OF_INT256).to_byte_array(signed=True)),
            (Opcode.OVER, b''),
            (Opcode.OVER, b''),

            (Opcode.JMPGE, Integer(44).to_byte_array(signed=True)),
            (Opcode.PUSHDATA1, (Integer(constants.SIZE_OF_INT256).to_byte_array(signed=True)
                                + bytes(constants.SIZE_OF_INT256))),
            (Opcode.REVERSE3, b''),
            (Opcode.SUB, b''),
            (Opcode.LEFT, b''),
            (Opcode.CAT, b''),

            (Opcode.JMP, Integer(4).to_byte_array()),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),

            (Opcode.CONVERT, StackItemType.ByteString),  # convert to uint256
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSHINT8, Integer(constants.SIZE_OF_INT256).to_byte_array(signed=True)),
            (Opcode.NUMEQUAL, b''),
            (Opcode.ASSERT, b''),
        ]

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_object.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return UInt256Method(self.return_type, value)
        return super().build(value)
