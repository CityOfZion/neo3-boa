from typing import Optional

from boa3.internal.neo3.core.types import UInt160
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract


class TestRunnerContract(TestContract):
    def __init__(self, contract_name: str, contract_hex_hash: str):
        self._name: str = contract_name
        self._contract_hash: str = contract_hex_hash

        super().__init__(None, None)
        self._script_hash = self._get_script_hash()

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return super().path

    @path.setter
    def path(self, value: str):
        self._nef_path = value

    def _get_script_hash(self) -> Optional[bytes]:
        try:
            return UInt160.from_string(self._contract_hash[2:]
                                       if self._contract_hash.startswith('0x')
                                       else self._contract_hash
                                       ).to_array()
        except BaseException:
            return None

    def is_valid_identifier(self, item: str) -> bool:
        if super().is_valid_identifier(item):
            return True

        # name is also a valid identifier
        return item == self._name
