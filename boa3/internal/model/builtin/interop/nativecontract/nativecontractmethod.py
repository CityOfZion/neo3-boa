import ast
from typing import Dict, List, Optional

from boa3.internal.compiler.compiledmetadata import CompiledMetadata
from boa3.internal.model.builtin.interop.contractgethashmethod import ContractGetHashMethod
from boa3.internal.model.builtin.interop.interopmethod import InteropMethod
from boa3.internal.model.type.itype import IType
from boa3.internal.model.variable import Variable


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
        self._added_to_permissions = False
        self._pack_arguments = None   # defined during compilation
        self._method_token_id = None  # defined during compilation
        self.external_name = self._sys_call

    @property
    def contract_script_hash(self) -> bytes:
        return self.script_hash_method.script_hash

    def reset(self):
        # reset the object state to ensure the correct output when calling consecutive compilations
        super().reset()
        self._added_to_permissions = False
        self._pack_arguments = None
        self._method_token_id = None

    def generate_internal_opcodes(self, code_generator):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.model.type.type import Type

        self._add_to_contract_permissions()

        call_flag = self._call_flags_default
        self_method_token_id = self._get_method_token_id(call_flag)

        if isinstance(self_method_token_id, int) and self_method_token_id >= 0:
            code_generator.convert_method_token_call(self_method_token_id)
        else:
            if self._pack_arguments is None:
                self._pack_arguments = False

            code_generator.convert_new_array(len(self.args))
            code_generator.convert_literal(call_flag)
            code_generator.convert_literal(self.method_name)
            code_generator.convert_builtin_method_call(self.script_hash_method, is_internal=True)
            code_generator.convert_builtin_method_call(Interop.CallContract, is_internal=True)

            if self.return_type is Type.none:
                code_generator.remove_stack_top_item()

    def _get_method_token_id(self, call_flag=None) -> Optional[int]:
        if self._method_token_id is None:
            from boa3.internal.compiler.codegenerator.vmcodemapping import VMCodeMapping

            if call_flag is None:
                call_flag = self._call_flags_default
            self._method_token_id = VMCodeMapping.instance().add_method_token(self, call_flag)
        return self._method_token_id

    def _add_to_contract_permissions(self):
        if not self._added_to_permissions:
            CompiledMetadata.instance().add_contract_permission(self.contract_script_hash, self._sys_call)
            self._added_to_permissions = True

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
