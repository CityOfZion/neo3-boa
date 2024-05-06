from typing import Any, Self

from boa3.internal.neo.smart_contract.notification import Notification
from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract


class TestRunnerNotification(Notification):
    _script_hash_key = 'contract'
    _value_key = 'state'

    def __init__(self, event_name: str, script_hash: bytes, *value: Any):
        super().__init__(event_name, script_hash, *value)
        self._contract = None

    @property
    def contract(self) -> TestContract:
        return self._contract

    @classmethod
    def from_json(
            cls,
            json: dict[str, Any],
            contract_collection: ContractCollection = None,
            *args,
            **kwargs
    ) -> Self:

        result = super().from_json(json)
        if result is None:
            return result

        if isinstance(contract_collection, ContractCollection) and result.origin in contract_collection:
            result._contract = contract_collection[result.origin]
        return result

    @classmethod
    def _get_script_from_str(cls, script: str) -> bytes:
        if isinstance(script, str):
            if script.startswith('0x'):
                str_script = script[2:]
            else:
                str_script = script
            script = UInt160.from_string(str_script).to_array()

        return script
