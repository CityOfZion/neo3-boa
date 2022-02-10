from typing import List

from boa3_test.tests.test_classes.testcontract import TestContract


class ContractCollection:
    def __init__(self):
        self._internal_list: List[TestContract] = []

    def append(self, new_contract: TestContract):
        return self._internal_list.append(new_contract)

    def remove(self, contract: TestContract):
        return self._internal_list.remove(contract)

    def clear(self):
        return self._internal_list.clear()

    def __len__(self):
        return len(self._internal_list)

    def __contains__(self, item) -> bool:
        return any(contract.is_valid_identifier(item) for contract in self._internal_list)

    def __getitem__(self, item) -> TestContract:
        return next((contract for contract in self._internal_list if contract.is_valid_identifier(item)), None)

    def __str__(self):
        return str(self._internal_list)

    def __repr__(self):
        return self._internal_list.__repr__()
