from typing import List

from boa3.internal import constants
from boa3_test.tests.test_classes.testcontract import TestContract


class ContractCollection:
    def __init__(self):
        self._internal_list: List[TestContract] = []

    def append(self, new_contract: TestContract):
        return self._internal_list.append(new_contract)

    def remove(self, contract: TestContract):
        return self._internal_list.remove(contract)

    def pop(self, index: int):
        return self._internal_list.pop(index)

    def clear(self):
        return self._internal_list.clear()

    def copy(self):
        collection_copy = ContractCollection()
        collection_copy._internal_list = self._internal_list.copy()
        return collection_copy

    def __len__(self):
        return len(self._internal_list)

    def __contains__(self, item) -> bool:
        return any(contract.is_valid_identifier(item) for contract in self._internal_list)

    def __getitem__(self, item) -> TestContract:
        from boa3.internal.neo3.core.types import UInt160
        if isinstance(item, UInt160):
            item = str(item)
        elif isinstance(item, bytes) and len(item) == constants.SIZE_OF_INT160:
            item = str(UInt160(item))
        return next((contract for contract in self._internal_list if contract.is_valid_identifier(item)), None)

    def __iter__(self):
        return self._internal_list.__iter__()

    def __str__(self):
        return str(self._internal_list)

    def __repr__(self):
        return self._internal_list.__repr__()
