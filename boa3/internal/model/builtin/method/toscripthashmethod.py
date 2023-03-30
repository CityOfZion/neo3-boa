from typing import Any, Dict, List, Optional, Sized, Tuple

from boa3.internal.compiler.codegenerator import get_bytes_count
from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.expression import IExpression
from boa3.internal.model.type.primitive.primitivetype import PrimitiveType
from boa3.internal.model.type.type import IType, Type
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode import OpcodeHelper
from boa3.internal.neo.vm.opcode.Opcode import Opcode


class ScriptHashMethod(IBuiltinMethod):

    def __init__(self, data_type: IType = None):
        if (not Type.int.is_type_of(data_type)
                and not Type.str.is_type_of(data_type)
                and not Type.bytes.is_type_of(data_type)):
            data_type = Type.any

        identifier = 'to_script_hash'
        args: Dict[str, Variable] = {'self': Variable(data_type)}
        from boa3.internal.model.type.collection.sequence.uint160type import UInt160Type
        super().__init__(identifier, args, return_type=UInt160Type.build())

    @property
    def identifier(self) -> str:
        from boa3.internal.model.type.type import Type
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
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.constants import SIZE_OF_INT160
        from boa3.internal.model.builtin.interop.crypto import Sha256Method
        from boa3.internal.model.builtin.interop.crypto import Ripemd160Method
        from boa3.internal.model.builtin.interop.stdlib.base58decodemethod import Base58DecodeMethod
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.Integer import Integer

        raise_exception_if_size_is_wrong = [
            (Opcode.JMP, b''),
            (Opcode.DROP, b''),
            (Opcode.DROP, b''),
            (Opcode.THROW, b''),
        ]
        raise_exception_if_size_is_wrong[0] = OpcodeHelper.get_jump_and_data(Opcode.JMPGE, get_bytes_count(raise_exception_if_size_is_wrong))

        except_use_hash_160 = Sha256Method().opcode + Ripemd160Method().opcode
        end_try = [
            (Opcode.ENDTRY, b'')
        ]
        end_try[-1] = OpcodeHelper.get_jump_and_data(Opcode.ENDTRY, get_bytes_count(end_try))

        try_to_decode_with_base58 = [
            (Opcode.DUP, b''),
            (Opcode.ISTYPE, Type.str.stack_item),
            (Opcode.JMPIF, Integer(4).to_byte_array(min_length=1)),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.DUP, b''),
        ] + Base58DecodeMethod().opcode + [
            (Opcode.DUP, b''),  # check if size is UInt160 + 1  // first position will be ignored
            (Opcode.SIZE, b''),
            OpcodeHelper.get_push_and_data(SIZE_OF_INT160 + 1),
            (Opcode.SWAP, b''),
            (Opcode.OVER, b''),
        ] + raise_exception_if_size_is_wrong + [
            (Opcode.DEC, b''),
            OpcodeHelper.get_push_and_data(1),
            (Opcode.SWAP, b''),
            (Opcode.SUBSTR, b''),
            (Opcode.CONVERT, Type.str.stack_item),
            (Opcode.NIP, b''),
            OpcodeHelper.get_jump_and_data(Opcode.JMP, get_bytes_count(except_use_hash_160)),
        ]

        try_code = OpcodeHelper.get_try_and_data(get_bytes_count(try_to_decode_with_base58), jump_through=True)
        begin_try = (
            [
                try_code
            ]
            + try_to_decode_with_base58
            + except_use_hash_160
            + end_try
        )

        return begin_try

    @property
    def _args_on_stack(self) -> int:
        return len(self.args)

    @property
    def _body(self) -> Optional[str]:
        return None

    def build(self, value: Any) -> IBuiltinMethod:
        if 'self' in self.args and self.args['self'].type is not Type.any:
            return self

        from boa3.internal.model.type.collection.sequence.ecpointtype import ECPointType
        from boa3.internal.model.type.primitive.inttype import IntType
        from boa3.internal.model.type.primitive.strtype import StrType
        from boa3.internal.model.type.primitive.bytestype import BytesType

        if isinstance(value, Sized) and len(value) == 1:
            value = value[0]

        if isinstance(value, ECPointType):
            from boa3.internal.model.builtin.method.ecpointtoscripthashmethod import ECPointToScriptHashMethod
            return ECPointToScriptHashMethod()
        elif isinstance(value, (IntType, StrType, BytesType)):
            return ScriptHashMethod(value)
        elif isinstance(value, IType):
            return ScriptHashMethod(Type.bytes)
        return super().build(value)
