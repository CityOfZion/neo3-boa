from typing import Any

from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke
from boa3_test.test_drive.model.invoker.neoinvokeresult import NeoInvokeResult
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.model.wallet.account import Account

__all__ = ['NeoInvokeCollection']


class NeoInvokeCollection:
    def __init__(self):
        self._internal_list: list[NeoInvoke] = []
        self._invoke_results: list[NeoInvokeResult] = []
        self._pending_results: list[NeoInvokeResult] = []

    def create_contract_invoke(self, contract: TestContract, operation: str, *args: Any) -> NeoInvoke:
        invoker = NeoInvoke(contract.name, operation, *args)
        invoker._contract = contract
        return invoker

    def append_contract_invoke(self, contract: TestContract, operation: str, *args: Any,
                               expected_result_type: type = None) -> NeoInvokeResult:
        invoker = NeoInvoke(contract.name, operation, *args)
        invoker._contract = contract
        invoke_result = NeoInvokeResult(invoker, expected_result_type=expected_result_type)
        self._internal_list.append(invoker)
        self._invoke_results.append(invoke_result)
        self._pending_results.append(invoke_result)
        return invoke_result

    def clear(self, *, state: VMState = VMState.HALT):
        pending_results = self._pending_results.copy()
        self._invoke_results.clear()
        self._pending_results.clear()

        if state != VMState.HALT:
            for pending_invoke in pending_results:
                pending_invoke.cancel()
        return self._internal_list.clear()

    def to_json(self):
        if len(self._internal_list) > 0:
            return [invoke.to_json() for invoke in self._internal_list]

        return [{}]

    def set_results(self, new_result_stack: list[Any], calling_account: Account | None = None) -> list[NeoInvokeResult]:
        no_iterations = min(len(new_result_stack), len(self._pending_results)) + 1
        pending_results = self._pending_results.copy()

        for index in range(1, no_iterations):
            invoke_result = self._pending_results.pop(0)
            invoke_result.invoke._invoker = calling_account
            invoke_result._result = new_result_stack[-index]

        return pending_results
