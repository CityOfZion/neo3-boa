import ast
from typing import Dict, List, Tuple, Optional

from boa3.internal.compiler.compiledmetadata import CompiledMetadata
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.opcode.OpcodeInfo import OpcodeInfo


class NativeContractMethod(InteropMethod):

    def __init__(self, native_contract_script_hash_method: ContractGetHashMethod, identifier: str, syscall: str,
                 args: Dict[str, Variable] = None, defaults: List[ast.AST] = None, return_type: IType = None,
                 internal_call_args: int = None):
        super().__init__(identifier, syscall, args, defaults, return_type)
        self.script_hash_method = native_contract_script_hash_method
        min_no_args = len(self.args_without_default)
        if not isinstance(internal_call_args, int):
            internal_call_args = len(self.args)
        elif len(self.args_without_default) > internal_call_args:
            internal_call_args = min_no_args

        self.internal_call_args = internal_call_args

        from boa3.internal.neo3.contracts.contracttypes import CallFlags
        self._call_flags_default = CallFlags.ALL
        self._pack_arguments = None   # defined during compilation
        self._method_token_id = None  # defined during compilation
        self.external_name = self._sys_call

    @property
    def contract_script_hash(self) -> bytes:
        return self.script_hash_method.script_hash

    def reset(self):
        # reset the object state to ensure the correct output when calling consecutive compilations
        super().reset()
        self._pack_arguments = None
        self._method_token_id = None

    @property
    def _opcode(self) -> List[Tuple[Opcode, bytes]]:
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.type.type import Type
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String

        call_flag = self._call_flags_default
        if self._pack_arguments is None:
            self._pack_arguments = False

        CompiledMetadata.instance().add_contract_permission(self.contract_script_hash, self._sys_call)
        self_method_token_id = self._get_method_token_id(call_flag)

        if isinstance(self_method_token_id, int) and self_method_token_id >= 0:
            call_opcode = Opcode.CALLT
            opcode_info = OpcodeInfo.get_info(call_opcode)
            arg_size = opcode_info.data_len

            call_opcodes = [
                (call_opcode, Integer(self_method_token_id).to_byte_array(min_length=arg_size))
            ]
        else:
            if len(self.args) == 0:
                pack_args = [(Opcode.NEWARRAY0, b'')]
            else:
                from boa3.internal.neo.vm.opcode import OpcodeHelper
                pack_args = [
                    OpcodeHelper.get_push_and_data(len(self.args)),
                    (Opcode.PACK, b'')
                ]

            call_flags = Integer(call_flag).to_byte_array(signed=True, min_length=1)
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

            call_opcodes = (pack_args
                            + flags_opcode
                            + method_opcode
                            + self.script_hash_method.opcode
                            + Interop.CallContract.opcode
                            + drop_if_void_opcode
                            )

        return call_opcodes

    def _get_method_token_id(self, call_flag=None) -> Optional[int]:
        if self._method_token_id is None:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping

            if call_flag is None:
                call_flag = self._call_flags_default
            self._method_token_id = VMCodeMapping.instance().add_method_token(self, call_flag)
        return self._method_token_id

    @property
    def pack_arguments(self) -> bool:
        if self._pack_arguments is None:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping
            self_method_token_id = self._get_method_token_id(self._call_flags_default)

            self._pack_arguments = not isinstance(self_method_token_id, int) or self_method_token_id < 0
        return self._pack_arguments

    @property
    def method_name(self) -> str:
        return self._sys_call
