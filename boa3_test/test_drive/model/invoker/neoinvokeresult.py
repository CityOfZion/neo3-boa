from typing import Type, Iterable

from boa3_test.test_drive.model.invoker import invokeresult
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke


class NeoInvokeResult:
    def __init__(self, invoke: NeoInvoke, expected_result_type: Type = None):
        self._invoke: NeoInvoke = invoke
        self._result = invokeresult.NOT_EXECUTED

        if not isinstance(expected_result_type, type):
            expected_result_type = None
        self._expected_result_type = expected_result_type

    @property
    def invoke(self) -> NeoInvoke:
        return self._invoke

    @property
    def result(self):
        if hasattr(self._result, 'copy'):
            result = self._result.copy()
        else:
            result = self._result

        if self._expected_result_type is not None:
            if self._expected_result_type is not str and isinstance(result, str):
                from boa3.internal.neo.vm.type.String import String
                result = String(result).to_bytes()

            if self._expected_result_type in (bool, int):
                if isinstance(result, bytes):
                    from boa3.internal.neo.vm.type.Integer import Integer
                    result = Integer.from_bytes(result, signed=True)

                if self._expected_result_type is bool and isinstance(result, int) and result in (False, True):
                    result = bool(result)

            elif self._expected_result_type is bytearray and isinstance(result, bytes):
                result = bytearray(result)
            elif self._expected_result_type is tuple and isinstance(result, Iterable):
                result = tuple(result)

        return result

    def cancel(self):
        if self._result is invokeresult.NOT_EXECUTED:
            self._result = invokeresult.CANCELED

    def __repr__(self):
        return f'{self._invoke.__repr__()} -> {self._result.__repr__()}'
