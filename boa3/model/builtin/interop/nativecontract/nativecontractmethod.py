import ast
from typing import Dict, List, Tuple

from boa3.model.builtin.interop.interopmethod import InteropMethod
from boa3.model.builtin.method import IBuiltinMethod
from boa3.model.type.itype import IType
from boa3.model.variable import Variable
from boa3.neo.vm.opcode.Opcode import Opcode


class NativeContractMethod(InteropMethod):

    def __init__(self, native_contract_script_hash_method: IBuiltinMethod, identifier: str, syscall: str,
                 args: Dict[str, Variable] = None, defaults: List[ast.AST] = None, return_type: IType = None):
        super().__init__(identifier, syscall, args, defaults, return_type)
        self.native_contract_script_hash_method = native_contract_script_hash_method

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.model.builtin.interop.interop import Interop
        from boa3.model.type.type import Type
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String
        from boa3.neo3.contracts import CallFlags

        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        flags_opcode = [
            (Opcode.PUSHDATA1, Integer(len(call_flags)).to_byte_array() + call_flags)
        ]
        method = String(self._sys_call).to_bytes()
        method_opcode = [
            (Opcode.PUSHDATA1, Integer(len(method)).to_byte_array(min_length=1) + method)
        ]
        drop_if_void_opcode = [
            (Opcode.DROP, b'')
        ] if self.return_type is Type.none else []

        return (flags_opcode
                + method_opcode
                + self.native_contract_script_hash_method.opcode
                + Interop.CallContract.opcode
                + drop_if_void_opcode
                )

    @property
    def pack_arguments(self) -> bool:
        return True

    @property
    def method_name(self) -> str:
        return self._sys_call
