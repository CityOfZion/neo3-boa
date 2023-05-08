from __future__ import annotations

import base64
from typing import Any, Dict, Optional

from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.test_drive.model.smart_contract.contractcollection import ContractCollection
from boa3_test.test_drive.model.smart_contract.testcontract import TestContract


class TestRunnerStorage:
    _storage_contract_name_key = 'name'
    _storage_contract_hash_key = 'hash'
    _storage_contract_values_key = 'values'
    _storage_key_key = 'key'
    _storage_item_key = 'value'

    def __init__(self, contract: TestContract, values: Dict[StorageKey, StorageItem]):
        self._contract: TestContract = contract
        self._values: Dict[StorageKey, StorageItem] = values

    @property
    def contract(self) -> Optional[TestContract]:
        if isinstance(self._contract, TestContract):
            return self._contract
        return None

    @property
    def values(self) -> Dict[StorageKey, StorageItem]:
        return self._values

    @classmethod
    def from_json(cls, json: Dict[str, Any], contracts: ContractCollection = None) -> TestRunnerStorage:
        keys = set(json.keys())
        if not keys.issubset([cls._storage_contract_name_key,
                              cls._storage_contract_hash_key,
                              cls._storage_contract_values_key]):
            return None

        contract_name = json[cls._storage_contract_name_key]
        contract_hash = json[cls._storage_contract_hash_key]
        if contract_name in contracts:
            contract = contracts[contract_name]
        elif contract_hash in contracts:
            contract = contracts[contract_hash]
        else:
            contract = None

        storage = {}
        storage_required_fields = [cls._storage_key_key, cls._storage_item_key]
        for item_json in json[cls._storage_contract_values_key]:
            if not set(item_json.keys()).issubset(storage_required_fields):
                continue

            key = StorageKey.from_json(item_json[cls._storage_key_key])
            item = StorageItem.from_json(item_json[cls._storage_item_key])

            storage[key] = item

        return cls(contract, storage)

    def is_valid_identifier(self, item: str) -> bool:
        if isinstance(self._contract, TestContract):
            return self._contract.is_valid_identifier(item)

        return False

    def __str__(self) -> str:
        return str(self._values)

    def __repr__(self) -> str:
        return self._values.__repr__()


class StorageKey:
    def __init__(self, key: bytes):
        self._key: bytes = key

    @classmethod
    def from_json(cls, json: str) -> StorageKey:
        decoded: bytes = base64.b64decode(json)
        return cls(decoded)

    def as_str(self) -> str:
        return String.from_bytes(self._key)

    def as_bytes(self) -> bytes:
        return self._key

    def __str__(self):
        return self.as_str()

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return self._key.__hash__()

    def __eq__(self, other) -> bool:
        return (other == self.as_bytes()
                or other == self.as_str()
                or (isinstance(other, StorageKey) and self._key == other._key))


class StorageItem:
    def __init__(self, value: bytes):
        self._value: bytes = value

    @classmethod
    def from_json(cls, json: str) -> StorageItem:
        decoded: bytes = base64.b64decode(json)
        return cls(decoded)

    def as_bytes(self) -> bytes:
        return self._value

    def as_str(self) -> str:
        return String.from_bytes(self._value)

    def as_int(self) -> int:
        return Integer.from_bytes(self._value)

    def __str__(self) -> str:
        return self._value.__str__()

    def __repr__(self):
        return str(self)

    def __hash__(self) -> int:
        return self._value.__hash__()

    def __eq__(self, other) -> bool:
        return (other == self.as_bytes()
                or other == self.as_int()
                or other == self.as_str()
                or (isinstance(other, StorageItem) and self._value == other._value))
