from typing import List

from boa3.internal import constants
from boa3.internal.neo import to_hex_str
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.testrunner.blockchain.contract import TestRunnerContract


class ContractCollection:

    _native_contracts = [
        TestRunnerContract('OracleContract', to_hex_str(constants.ORACLE_SCRIPT)),
        TestRunnerContract('RoleManagement', to_hex_str(constants.ROLE_MANAGEMENT)),
        TestRunnerContract('PolicyContract', to_hex_str(constants.POLICY_SCRIPT)),
        TestRunnerContract('GasToken', to_hex_str(constants.GAS_SCRIPT)),
        TestRunnerContract('NeoToken', to_hex_str(constants.NEO_SCRIPT)),
        TestRunnerContract('LedgerContract', to_hex_str(constants.LEDGER_SCRIPT)),
        TestRunnerContract('CryptoLib', to_hex_str(constants.CRYPTO_SCRIPT)),
        TestRunnerContract('StdLib', to_hex_str(constants.STD_LIB_SCRIPT)),
        TestRunnerContract('ContractManagement', to_hex_str(constants.MANAGEMENT_SCRIPT)),
    ]

    def __init__(self):
        natives = self._native_contracts.copy()

        self._contract_names: List[str] = [native.name for native in natives]
        self._contract_paths: List[str] = [native.path for native in natives]
        self._internal_list: List[TestContract] = natives
        self._waiting_deploy: List[TestContract] = []

    def append(self, new_contract: TestContract):
        if not isinstance(new_contract, TestContract):
            return
        if new_contract.name not in self._contract_names:
            self._contract_names.append(new_contract.name)
            self._contract_paths.append(new_contract.path)
            if new_contract.script_hash is None:
                self._waiting_deploy.append(new_contract)
            return self._internal_list.append(new_contract)

    def remove(self, contract: TestContract):
        try:
            contract_index = self._contract_names.index(contract.name)
            self._contract_names.pop(contract_index)
            self._contract_paths.pop(contract_index)
            contract = self._internal_list.pop(contract_index)
            if contract.script_hash is None:
                self._waiting_deploy.remove(contract)
        except ValueError:
            return

    def pop(self, index: int = -1):
        self._contract_names.pop(index)
        self._contract_paths.pop(index)
        contract = self._internal_list.pop(index)
        if contract.script_hash is None:
            self._waiting_deploy.remove(contract)
        return contract

    def clear(self):
        self._contract_names.clear()
        self._contract_paths.clear()
        self._waiting_deploy.clear()
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
                    self._waiting_deploy.remove(existing_contract)

                already_existing_contracts.remove(contract.name)
                contract_indexes.remove(contract_index)
            except ValueError:
                self.append(contract)

        # these contracts were destroyed in the test blockchain
        for removed_index in reversed(contract_indexes):
            self._contract_names.pop(removed_index)
            self._contract_paths.pop(removed_index)
            contract = self._internal_list.pop(removed_index)
            if contract.script_hash is None:
                self._waiting_deploy.remove(contract)

    def update_after_deploy(self):
        for contract in self._waiting_deploy.copy():
            script_hash = contract.script_hash
            if script_hash is not None:
                self._waiting_deploy.remove(contract)
