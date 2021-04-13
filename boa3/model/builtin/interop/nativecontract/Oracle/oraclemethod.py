import ast
from typing import Dict, List, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class OracleMethod(InteropMethod):

    def __init__(self, identifier: str, native_identifier: str, args: Dict[str, Variable] = None,
                 defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(identifier, native_identifier, args, defaults, return_type)

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String

        method = String(self._sys_call).to_bytes()
        method_opcode = [
            (Opcode.PUSHDATA1, Integer(len(method)).to_byte_array(min_length=1) + method)
        ]
        drop_if_void_opcode = [
            (Opcode.DROP, b'')
        ] if self.return_type is Type.none else []

        return (method_opcode
                + Interop.OracleScriptHash.getter.opcode
                + Interop.CallContract.opcode
                + drop_if_void_opcode
                )

    @property
    def pack_arguments(self) -> bool:
        return True

    @property
    def method_name(self) -> str:
        return self._sys_call
