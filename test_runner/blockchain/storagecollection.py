from typing import List

from test_runner.blockchain.storage import TestRunnerStorage


class StorageCollection:
    def __init__(self):
        self._internal_list: List[TestRunnerStorage] = []

    def append(self, new_storage: TestRunnerStorage):
        return self._internal_list.append(new_storage)

    def remove(self, storage: TestRunnerStorage):
        return self._internal_list.remove(storage)

    def clear(self):
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
