from typing import Any, Dict, List, Optional, Sized, Tuple

from boa3.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.model.expression import IExpression
from boa3.model.type.primitive.primitivetype import PrimitiveType
from boa3.model.type.type import IType, Type
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class ScriptHashMethod(IBuiltinMethod):

    def __init__(self, data_type: IType = None):
        if (not Type.int.is_type_of(data_type)
                and not Type.str.is_type_of(data_type)
                and not Type.bytes.is_type_of(data_type)):
            data_type = Type.any

        identifier = 'to_script_hash'
        args: Dict[str, Variable] = {'self': Variable(data_type)}
        super().__init__(identifier, args, return_type=Type.bytes)

    @property
    def identifier(self) -> str:
        from boa3.model.type.type import Type
        self_type = self.args['self'].type
        if self_type is Type.any:
            return self._identifier
        return '-{0}_from_{1}'.format(self._identifier, self_type._identifier)

    def validate_parameters(self, *params: IExpression) -> bool:
        if len(params) != 1:
            return False
        if not isinstance(params[0], IExpression):
            return False
        return isinstance(params[0].type, PrimitiveType)

    @property
    def is_supported(self) -> bool:
        return self.args['self'].type is not Type.any

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.constants import SIZE_OF_INT160
        from boa3.model.builtin.interop.stdlib.base58decodemethod import Base58DecodeMethod
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer

        opcodes = [
            (Opcode.DUP, b''),      # convert value to string
            (Opcode.SIZE, b''),
            (Opcode.JMPIFNOT, Integer(36).to_byte_array(signed=True, min_length=1)),
            (Opcode.DUP, b''),      # convert value to string
            (Opcode.ISTYPE, Type.str.stack_item),
            (Opcode.JMPIF, Integer(4).to_byte_array(min_length=1)),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.PUSH1, b''),
            (Opcode.PACK, b'')
        ]
        opcodes.extend(Base58DecodeMethod().opcode)
        script_len = Integer(SIZE_OF_INT160).to_byte_array(min_length=1)
        opcodes.extend([
            (Opcode.DUP, b''),      # if len(result) > SIZE_OF_INT160, truncates the result
            (Opcode.SIZE, b''),
            (Opcode.PUSHDATA1, Integer(len(script_len)).to_byte_array(min_length=1) + script_len),
            (Opcode.CONVERT, Type.int.stack_item),
            (Opcode.JMPGT, Integer(8).to_byte_array(min_length=1, signed=True)),
            (Opcode.DUP, b''),
            (Opcode.SIZE, b''),     # first byte identifies address version
            (Opcode.DEC, b''),
            (Opcode.RIGHT, b''),
            (Opcode.JMP, Integer(9).to_byte_array(min_length=1, signed=True)),
            (Opcode.PUSH1, b''),
            (Opcode.PUSHDATA1, Integer(len(script_len)).to_byte_array(min_length=1) + script_len),
            (Opcode.CONVERT, Type.int.stack_item),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.bytes.stack_item)
        ])
        return opcodes

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if 'self' in self.args and self.args['self'].type is not Type.any:
            return self

        from boa3.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.model.type.primitive.inttype import IntType
        from boa3.model.type.primitive.strtype import StrType
        from boa3.model.type.primitive.bytestype import BytesType

        if isinstance(value, Sized) and len(value) == 1:
            value = value[0]

        if isinstance(value, ECPointType):
            from boa3.model.builtin.method.ecpointtoscripthashmethod import ECPointToScriptHashMethod
            return ECPointToScriptHashMethod()
        elif isinstance(value, (IntType, StrType, BytesType)):
            return ScriptHashMethod(value)
        elif isinstance(value, IType):
            return ScriptHashMethod(Type.bytes)
        return super().build(value)
