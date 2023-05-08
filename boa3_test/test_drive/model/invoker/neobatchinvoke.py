from typing import Type, Iterable

from boa3_test.test_drive.model.interface.itransactionobject import ITransactionObject
from boa3_test.test_drive.model.invoker import invokeresult
from boa3_test.test_drive.model.invoker.neoinvoke import NeoInvoke


class NeoBatchInvoke(ITransactionObject):
    def __init__(self, invoke: NeoInvoke, tx_pos: int, expected_result_type: Type = None):
        super().__init__()
        self._invoke: NeoInvoke = invoke
        self._tx_pos: int = tx_pos
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

    def _set_data_from_match_result(self, match_groups: dict):
        super()._set_data_from_match_result(match_groups)
        if self._tx_id is not None and self._result is not invokeresult.TRANSACTION_EXECUTED:
            self._result = invokeresult.TRANSACTION_EXECUTED

    def __repr__(self):
        return f'{self._invoke.__repr__()} -> {self.tx_id.__repr__()}'
