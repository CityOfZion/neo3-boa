from typing import List

from boa3_test.test_drive.model.smart_contract.testcontract import TestContract


class ContractCollection:
    def __init__(self):
        self._contract_names: List[str] = []
        self._contract_paths: List[str] = []
        self._internal_list: List[TestContract] = []

    def append(self, new_contract: TestContract):
        if not isinstance(new_contract, TestContract):
            return
        if new_contract.name not in self._contract_names:
            self._contract_names.append(new_contract.name)
            self._contract_paths.append(new_contract.path)
            return self._internal_list.append(new_contract)

    def remove(self, contract: TestContract):
        try:
            contract_index = self._contract_names.index(contract.name)
            self._contract_names.pop(contract_index)
            self._contract_paths.pop(contract_index)
            self._internal_list.pop(contract_index)
        except ValueError:
            return

    def pop(self, index: int = -1):
        self._contract_names.pop(index)
        self._contract_paths.pop(index)
        return self._internal_list.pop(index)

    def clear(self):
        self._contract_names.clear()
        self._contract_paths.clear()
        return self._internal_list.clear()

    def __len__(self):
        return len(self._internal_list)

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            if item in self._contract_names:
                return True

            if item in self._contract_paths:
                return True

        if hasattr(item, 'name') and item.name in self._contract_names:
            return True

        return any(contract.is_valid_identifier(item) for contract in self._internal_list)

    def __getitem__(self, item) -> TestContract:
        if isinstance(item, str):
            try:
                try:
                    contract_index = self._contract_names.index(item)
                except ValueError:
                    contract_index = self._contract_paths.index(item)

                return self._internal_list[contract_index]
            except ValueError:
                pass

        return next((contract for contract in self._internal_list if contract.is_valid_identifier(item)), None)

    def __str__(self):
        return str(self._internal_list)

    def __repr__(self):
        return self._internal_list.__repr__()

    def replace(self, deployed_contracts: List[TestContract]):
        already_existing_contracts = self._contract_names.copy()
        contract_indexes = list(range(len(already_existing_contracts)))

        for contract in deployed_contracts:
            try:
                contract_index = self._contract_names.index(contract.name)
                existing_contract = self._internal_list[contract_index]
                if existing_contract.script_hash is None:
                    existing_contract.script_hash = contract.script_hash

                already_existing_contracts.remove(contract.name)
                contract_indexes.remove(contract_index)
            except ValueError:
                self.append(contract)

        # these contracts were destroyed in the test blockchain
        for removed_index in reversed(contract_indexes):
            self._contract_names.pop(removed_index)
            self._contract_paths.pop(removed_index)
            self._internal_list.pop(removed_index)
