from typing import Any, List

from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke
from boa3_test.test_drive.model.invoker.neoinvokeresult import NeoInvokeResult
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract


class NeoInvokeCollection:
    def __init__(self):
        self._internal_list: List[NeoInvoke] = []
        self._invoke_results: List[NeoInvokeResult] = []
        self._pending_results: List[NeoInvokeResult] = []

    def append_contract_invoke(self, contract: TestContract, operation: str, *args: Any) -> NeoInvokeResult:
        invoker = NeoInvoke(contract.name, operation, *args)
        invoke_result = NeoInvokeResult(invoker)
        self._internal_list.append(invoker)
        self._invoke_results.append(invoke_result)
        self._pending_results.append(invoke_result)
        return invoke_result

    def clear(self):
        self._invoke_results.clear()
        self._pending_results.clear()
        return self._internal_list.clear()

    def to_json(self):
        if len(self._internal_list) > 0:
            return [invoke.to_json() for invoke in self._internal_list]

        return [{}]

    def set_results(self, new_result_stack: List[Any]) -> List[NeoInvokeResult]:
        no_iterations = min(len(new_result_stack), len(self._pending_results)) + 1
        pending_results = self._pending_results.copy()

        for index in range(1, no_iterations):
            invoke_result = self._pending_results.pop(0)
            invoke_result._result = new_result_stack[-index]

        return pending_results
