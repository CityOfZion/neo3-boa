from typing import List, Union

from boa3_test.test_drive.model.smart_contract.testcontract import TestContract
from boa3_test.test_drive.testrunner.blockchain.storage import TestRunnerStorage, StorageKey


class StorageCollection:
    def __init__(self):
        self._internal_list: List[TestRunnerStorage] = []
        self._storage_contracts: List[TestContract] = []

    def append(self, new_storage: TestRunnerStorage):
        self._storage_contracts.append(new_storage.contract)
        return self._internal_list.append(new_storage)

    def remove(self, storage: TestRunnerStorage):
        try:
            index = self._internal_list.index(storage)
            self._storage_contracts.pop(index)
            self._internal_list.pop(index)
        except BaseException as e:
            raise e  # try except just to ensure that the value will be removed from both lists

    def get(self, storage_contract: TestContract, key: Union[bytes, str]):
        if isinstance(key, str):
            try:
                key = bytes(key)
            except TypeError:
                from boa3.internal import constants
                key = key.encode(encoding=constants.ENCODING)

        index = self._storage_contracts.index(storage_contract)
        try:
            storage = self._internal_list[index].values
            storage_key = StorageKey(key)

            return storage[storage_key]
        except:
            return None

    def clear(self):
        self._storage_contracts.clear()
        return self._internal_list.clear()

    def __len__(self):
        return len(self._internal_list)

    def __contains__(self, item) -> bool:
        return any(storage.is_valid_identifier(item) for storage in self._internal_list)

    def __getitem__(self, item) -> TestRunnerStorage:
        return next((storage for storage in self._internal_list if storage.is_valid_identifier(item)), None)

    def __str__(self):
        dict_repr = {}
        for storage in self._internal_list:
            contract_id = storage.contract
            if contract_id is not None:
                contract_id = contract_id.name if hasattr(contract_id, 'name') else contract_id.script_hash

            dict_repr[contract_id] = storage.values
        return str(dict_repr)

    def __repr__(self):
        return str(self)
