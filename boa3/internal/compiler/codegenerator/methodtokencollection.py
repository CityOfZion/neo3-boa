from typing import List, Optional

from boa3.internal.model.builtin.method.builtinmethod import IBuiltinMethod
from boa3.internal.model.type.type import Type
from boa3.internal.neo3.contracts import CallFlags
from boa3.internal.neo3.contracts.nef import MethodToken
from boa3.internal.neo3.core import types


class MethodTokenCollection:
    def __init__(self):
        self._method_tokens: List[MethodToken] = []
        self._called_builtins: List[IBuiltinMethod] = []

    def append(self, contract_method: IBuiltinMethod, call_flag: CallFlags = CallFlags.ALL) -> Optional[int]:
        method_token_id = self._try_get_index(contract_method, call_flag)
        if method_token_id is None and hasattr(contract_method, 'contract_script_hash'):
            method_token = MethodToken(hash=types.UInt160(contract_method.contract_script_hash),
                                       method=contract_method.external_name,
                                       parameters_count=(contract_method.internal_call_args
                                                         if hasattr(contract_method, 'internal_call_args')
                                                         else len(contract_method.args)),
                                       has_return_value=contract_method.return_type is not Type.none,
                                       call_flags=call_flag)

            if contract_method not in self._called_builtins:
                self._called_builtins.append(contract_method)

            if hasattr(contract_method, 'method_name') and len(contract_method.method_name) == 0:
                # it's a contract method with a different interface, so it shouldn't have its method token included
                return None

            method_token_id = len(self._method_tokens)
            if hasattr(contract_method, '_method_token_id'):
                contract_method.reset()
            self._method_tokens.append(method_token)

        return method_token_id

    def clear(self):
        # reset the opcodes to ensure the correct output when calling consecutive compilations
        for method in self._called_builtins:
            method.reset()

        self._called_builtins.clear()
        return self._method_tokens.clear()

    def _try_get_index(self, contract_method: IBuiltinMethod, call_flag: CallFlags = CallFlags.ALL) -> Optional[int]:
        if not hasattr(contract_method, 'contract_script_hash'):
            return None

        parameters_count = (contract_method.internal_call_args
                            if hasattr(contract_method, 'internal_call_args')
                            else len(contract_method.args))

        method_token_index = next((index for index, token in enumerate(self._method_tokens)
                                   if (token.hash.to_array() == contract_method.contract_script_hash
                                       and token.method == contract_method.external_name
                                       and token.parameters_count == parameters_count
                                       and token.has_return_value == (contract_method.return_type is not Type.none)
                                       and token.call_flags == call_flag)), None)
        return method_token_index

    def to_list(self) -> List[MethodToken]:
        return self._method_tokens.copy()

    def __getitem__(self, item):
        if isinstance(item, int) and len(self._method_tokens) > item:
            return self._method_tokens[item]
        else:
            return None
