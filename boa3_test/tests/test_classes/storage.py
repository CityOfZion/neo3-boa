from __future__ import annotations

from typing import Any, Dict, List, Union

from boa3.internal import constants
from boa3.internal.neo.utils import contract_parameter_to_json, stack_item_from_json
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.core.serialization import BinaryReader
from boa3_test.tests.test_classes.nativecontractprefix import get_native_contract_data


class Storage:
    def __init__(self):
        self._dict: Dict[StorageKey, StorageItem] = {}

    def pop(self, key: bytes) -> StorageItem:
        storage_key = StorageKey(key)
        return self._dict.pop(storage_key)

    def clear(self, delete_deploy_data: bool = True):
        prefix, native_id = get_native_contract_data(constants.MANAGEMENT_SCRIPT)
        for key in list(self._dict.keys()):
            should_delete = (key._ID > 0  # it's a deployd contract
                             or (delete_deploy_data
                                 and key._ID == native_id
                                 and key._key.startswith(prefix)  # it's a deployed contract register
                                 )
                             )
            if should_delete:
                # keep native contracts storage
                self._dict.pop(key)

    def copy(self) -> Storage:
        storage = Storage()
        storage._dict = self._dict.copy()
        return storage

    def to_json(self) -> List[Dict[str, Any]]:
        return [{'key': key.to_json(),
                 'value': item.to_json()
                 } for key, item in self._dict.items()
                ]

    @classmethod
    def from_json(cls, json: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Storage:
        if not isinstance(json, list):
            json = [json]

        new_storage = {}
        for storage_value in json:
            key = StorageKey.from_json(storage_value['key'])
            value = StorageItem.from_json(storage_value['value'])
            new_storage[key] = value

        storage = Storage()
        storage._dict = new_storage
        return storage

    def add_token(self, token_script: bytes, script_hash: bytes, amount: int) -> bool:
        if len(token_script) != 20 or len(script_hash) != 20 or amount <= 0:
            return False

        from boa3_test.tests.test_classes.nativecontractprefix import get_native_contract_data
        token_prefix, token_id = get_native_contract_data(token_script)
        if token_prefix is None or token_id is None:
            return False

        balance_key = token_prefix + script_hash
        if balance_key in self._dict:
            balance = Integer.from_bytes(self[balance_key])
        else:
            balance = 0

        balance += amount

        from boa3_test.tests.test_classes.nativeaccountstate import NativeAccountState
        key = StorageKey(balance_key)
        key._ID = token_id
        self._dict[key] = StorageItem(NativeAccountState(balance).serialize())
        return True

    def has_contract(self, script_hash: bytes) -> bool:
        prefix, native_id = get_native_contract_data(constants.MANAGEMENT_SCRIPT)
        if prefix is None or native_id is None:
            return False

        storage_key = self.build_key(prefix + script_hash, native_id)
        return storage_key in self

    def get_contract_id(self, script_hash: bytes) -> int:
        prefix, native_id = get_native_contract_data(constants.MANAGEMENT_SCRIPT)
        if prefix is None or native_id is None:
            return False

        storage_key = self.build_key(prefix + script_hash, native_id)
        if storage_key in self:
            result = self[storage_key]
            with BinaryReader(result) as reader:
                from boa3_test.tests.test_classes.binaryserializer import deserialize_binary
                result = deserialize_binary(reader)

            return result[0] if isinstance(result[0], int) else -1
        else:
            return -1

    def __contains__(self, item: StorageKey) -> bool:
        return item in self._dict

    def __getitem__(self, item: StorageKey) -> Any:
        return self._dict[item].value

    def __setitem__(self, key: StorageKey, value: Any):
        from boa3.internal.neo.vm.type import StackItem
        if isinstance(value, int):
            storage_value = Integer(value).to_byte_array()
        elif isinstance(value, str):
            storage_value = String(value).to_bytes()
        else:
            storage_value = StackItem.serialize(value)
        self._dict[key] = StorageItem(storage_value)

    @staticmethod
    def build_key(key: bytes, index: int) -> StorageKey:
        return StorageKey(key, index)


class StorageKey:
    def __init__(self, key: bytes, _id: int = 0):
        self._ID: int = _id
        self._key: bytes = key

    def to_json(self) -> Dict[str, Any]:
        return {'id': self._ID,
                'key': contract_parameter_to_json(self._key)
                }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> StorageKey:
        k = stack_item_from_json(json['key'])
        if isinstance(k, str):
            from boa3.internal.neo.vm.type.String import String
            k = String(k).to_bytes()

        key = StorageKey(k)
        key._ID = json['id']
        return key

    def __eq__(self, other) -> bool:
        return isinstance(other, StorageKey) and self._key == other._key and self._ID == other._ID

    def __str__(self) -> str:
        return '({0}, {1})'.format(self._key, self._ID)

    def __hash__(self) -> int:
        return self._key.__hash__()


class StorageItem:
    def __init__(self, value: bytes, is_constant: bool = False):
        self._is_constant: bool = is_constant
        self._value: bytes = value

    @property
    def value(self) -> bytes:
        return self._value

    def to_json(self) -> Dict[str, Any]:
        return {'isconstant': self._is_constant,
                'value': contract_parameter_to_json(self._value)
                }

    @classmethod
    def from_json(cls, json: Dict[str, Any]) -> StorageItem:
        value = stack_item_from_json(json['value'])
        if isinstance(value, str):
            from boa3.internal.neo.vm.type.String import String
            value = String(value).to_bytes()

        item = StorageItem(value, json['isconstant'])
        return item

    def __str__(self) -> str:
        return self._value.__str__()
