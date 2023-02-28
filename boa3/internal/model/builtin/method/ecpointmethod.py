from typing import Any, Dict, List, Optional, Tuple

from boa3.internal.compiler.codegenerator import get_bytes_count
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ECPointMethod(IBuiltinMethod):

    def __init__(self, return_type: ECPointType, argument_type: IType = None):
        from boa3.internal.model.type.type import Type
        if argument_type is None or not self.validate_parameters(argument_type):
            argument_type = Type.none

        identifier = 'ECPoint'
        args: Dict[str, Variable] = {'arg': Variable(argument_type)}

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

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.StackItem import StackItemType

        ECPOINT_SIZE = 33

        throw_if_invalid = [
            (Opcode.THROW, b''),
        ]
        check_bytestr_size = [
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),
            (Opcode.PUSHINT8, Integer(ECPOINT_SIZE).to_byte_array(signed=True)),
            OpcodeHelper.get_jump_and_data(Opcode.JMPEQ, get_bytes_count(throw_if_invalid), jump_through=True),
        ]

        return [
            (Opcode.CONVERT, StackItemType.ByteString),  # convert to ECPoint
            (Opcode.DUP, b''),
            (Opcode.ISNULL, b''),
            OpcodeHelper.get_jump_and_data(Opcode.JMPIF, get_bytes_count(check_bytestr_size), jump_through=True),
        ] + check_bytestr_size + throw_if_invalid

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return

    def build(self, value: Any) -> IBuiltinMethod:
        if type(value) == type(self._arg_arg.type):
            return self
        if isinstance(value, list):
            value = value[0] if len(value) > 0 else None
        if self.validate_parameters(value):
            return ECPointMethod(self.return_type, value)
        return super().build(value)
