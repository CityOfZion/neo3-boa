from __future__ import annotations

import abc
from typing import Tuple, Optional, Iterator

from boa3.neo3 import storage
from boa3.neo3.core import types
from boa3.neo3.network import payloads


class IDBImplementation(abc.ABC):
    def get_rawview(self):
        return RawView(self)

    @abc.abstractmethod
    def get_snapshotview(self) -> storage.Snapshot:
        """ Get a snapshot view of the database with caching. """

    def close(self):
        """ clean up any resources."""

    @abc.abstractmethod
    def _internal_bestblockheight_get(self):
        """ Get the best stored block height. """

    @abc.abstractmethod
    def _internal_bestblockheight_put(self, height: int):
        """ Persist a new best stored block height. """

    @abc.abstractmethod
    def _internal_bestblockheight_update(self, height: int):
        """ Update the existing best stored block height. """

    @abc.abstractmethod
    def _internal_block_put(self, block: payloads.Block) -> None:
        """ Persist a block to the real backend. """

    @abc.abstractmethod
    def _internal_block_update(self, block: payloads.Block) -> None:
        """ Update a block in the real backend. """

    @abc.abstractmethod
    def _internal_block_delete(self, hash: types.UInt256) -> None:
        """ Delete a block from the real backend."""

    @abc.abstractmethod
    def _internal_block_get(self, hash: types.UInt256) -> payloads.Block:
        """
        Get a block from the real backend.

        Must raise KeyError if not found. Return value must be read only.
        """

    def _internal_block_try_get(self, hash: types.UInt256) -> Optional[payloads.Block]:
        try:
            return self._internal_block_get(hash)
        except KeyError:
            return None

    @abc.abstractmethod
    def _internal_block_get_by_height(self, height: int) -> payloads.Block:
        """
        Try to get a block by height.

        Must raise KeyError if not found.
        """

    @abc.abstractmethod
    def _internal_block_all(self) -> Iterator[payloads.Block]:
        """ Return all blocks stored in the real backend (readonly). """

    @abc.abstractmethod
    def _internal_contract_put(self, contract: storage.ContractState) -> None:
        """ Persist a contract in the real backend. """

    @abc.abstractmethod
    def _internal_contract_update(self, contract: storage.ContractState) -> None:
        """ Update a contract in the real backend. """

    @abc.abstractmethod
    def _internal_contract_delete(self, script_hash: types.UInt160) -> None:
        """ Delete a contract from the real backend. """

    @abc.abstractmethod
    def _internal_contract_get(self, script_hash: types.UInt160) -> storage.ContractState:
        """
        Get a contract from the real backend.

        Must raise KeyError if not found. Return value must be read only.
        """

    def _internal_contract_try_get(self, script_hash: types.UInt160) -> Optional[storage.ContractState]:
        try:
            return self._internal_contract_get(script_hash)
        except KeyError:
            return None

    @abc.abstractmethod
    def _internal_contract_all(self) -> Iterator[storage.ContractState]:
        """ Return all contracts stored in the real backend (readonly). """

    @abc.abstractmethod
    def _internal_storage_put(self, key: storage.StorageKey, value: storage.StorageItem) -> None:
        """ Persist a storage key/value pair in the real backend. """

    @abc.abstractmethod
    def _internal_storage_update(self, key: storage.StorageKey, value: storage.StorageItem) -> None:
        """ Update a storage key/value pair in the real backend. """

    @abc.abstractmethod
    def _internal_storage_delete(self, key: storage.StorageKey) -> None:
        """ Delete a storage key/value pair from the real backend. """

    @abc.abstractmethod
    def _internal_storage_get(self, key: storage.StorageKey) -> storage.StorageItem:
        """
        Get a value by its key from the backend.

        Must raise KeyError if not found. Return value must be read only.
        """

    def _internal_storage_try_get(self, key: storage.StorageKey) -> Optional[storage.StorageItem]:
        try:
            return self._internal_storage_get(key)
        except KeyError:
            return None

    @abc.abstractmethod
    def _internal_storage_all(self, contract_script_hash: types.UInt160 = None) -> Iterator[
            Tuple[storage.StorageKey, storage.StorageItem]]:
        """ Return all storage pairs for a given smart contract stored in the real backend (readonly). """

    @abc.abstractmethod
    def _internal_storage_find(self, contract_script_hash: types.UInt160,
                               key_prefix: bytes) -> Iterator[Tuple[storage.StorageKey, storage.StorageItem]]:
        """ Find key/value pairs for a given smart contract by a given key prefix. """

    @abc.abstractmethod
    def _internal_transaction_put(self, transaction: payloads.Transaction) -> None:
        """ Persist a transaction in the real backend (readonly). """

    @abc.abstractmethod
    def _internal_transaction_update(self, transaction: payloads.Transaction) -> None:
        """ Update a transaction in the real backend. """

    @abc.abstractmethod
    def _internal_transaction_delete(self, hash: types.UInt256) -> None:
        """ Delete a transaction from the real backend. """

    @abc.abstractmethod
    def _internal_transaction_get(self, hash: types.UInt256) -> payloads.Transaction:
        """
        Get a transaction from the real backend.

        Must raise KeyError if not found. Return value must be read only.
        """

    def _internal_transaction_try_get(self, hash: types.UInt256) -> Optional[payloads.Transaction]:
        try:
            return self._internal_transaction_get(hash)
        except KeyError:
            return None

    @abc.abstractmethod
    def _internal_transaction_all(self) -> Iterator[payloads.Transaction]:
        """ Return all transactions stored in the real backend. """


class RawView:
    def __init__(self, db: IDBImplementation):
        self._db = db

    @property
    def blocks(self):
        return RawBlockAccess(self._db)

    @property
    def contracts(self):
        return RawContractAccess(self._db)

    @property
    def storages(self):
        return RawStorageAccess(self._db)

    @property
    def transactions(self):
        return RawTXAccess(self._db)

    @property
    def block_height(self):
        try:
            return self._db._internal_bestblockheight_get()
        except KeyError:
            return -1

    @block_height.setter
    def block_height(self, value):
        raise AttributeError("Can't set attribute on a raw view. view.blocks.put() automatically updates the height "
                             "when applicable")


class RawBlockAccess:
    def __init__(self, db: IDBImplementation):
        self._db = db

    def put(self, block: payloads.Block) -> None:
        """
        Store a block.

        Args:
            block: instance.
        """
        self._db._internal_block_put(block)

    def get(self, hash: types.UInt256) -> payloads.Block:
        """
        Retrieve a block.

        Args:
            hash: block hash.

        Raises:
            KeyError: if the item is not found.
        """
        return self._db._internal_block_get(hash)

    def try_get(self, hash: types.UInt256) -> Optional[payloads.Block]:
        """
        Try to retrieve a block.

        Args:
            hash: block hash.
        """
        return self._db._internal_block_try_get(hash)

    def get_by_height(self, height: int) -> payloads.Block:
        """
        Retrieve a block by its height.

        Args:
            height: target block index/height.
        """
        return self._db._internal_block_get_by_height(height)

    def try_get_by_height(self, height: int) -> Optional[payloads.Block]:
        """
        Try to retrieve a block by its height.

        Args:
            height: target block index/height.
        """
        try:
            return self.get_by_height(height)
        except KeyError:
            return None

    def delete(self, hash: types.UInt256) -> None:
        """
        Remove a block.

        Args:
            hash: block hash.
        """
        self._db._internal_block_delete(hash)

    def all(self) -> Iterator[payloads.Block]:
        """
        Retrieve all stored blocks.
        """
        for block in self._db._internal_block_all():
            yield block


class RawContractAccess:
    def __init__(self, db: IDBImplementation):
        self._db = db

    def put(self, contract: storage.ContractState) -> None:
        """
        Store a contract.

        Args:
            contract: contract state instance.
        """
        self._db._internal_contract_put(contract)

    def get(self, script_hash: types.UInt160) -> storage.ContractState:
        """
        Retrieve a contract.

        Args:
            script_hash: contract script hash.

        Raises:
            KeyError: if the item is not found.
        """
        return self._db._internal_contract_get(script_hash)

    def try_get(self, script_hash: types.UInt160) -> Optional[storage.ContractState]:
        """
        Try to retrieve a contract.

        Args:
            script_hash: contract script hash.
        """
        return self._db._internal_contract_try_get(script_hash)

    def delete(self, script_hash: types.UInt160) -> None:
        """
        Remove a transaction.

        Args:
            script_hash: contract script hash.
        """
        self._db._internal_contract_delete(script_hash)

    def all(self) -> Iterator[storage.ContractState]:
        """
        Retrieve all stored contracts.
        """
        for contract in self._db._internal_contract_all():
            yield contract


class RawStorageAccess:
    def __init__(self, db: IDBImplementation):
        self._db = db

    def put(self, key: storage.StorageKey, value: storage.StorageItem) -> None:
        """
        Store the value under the given key.

        Args:
            key: identifier to store the value under.
            value: the value to be persisted.
        """
        self._db._internal_storage_put(key, value)

    def get(self, key: storage.StorageKey) -> storage.StorageItem:
        """
        Retrieve a value from storage.

        Args:
            key: identifier.

        Raises:
            KeyError: if the item is not found.
        """
        return self._db._internal_storage_get(key)

    def try_get(self, key: storage.StorageKey) -> Optional[storage.StorageItem]:
        """
        Try to retrieve a value from storage.

        Args:
            key: identifier.
        """
        return self._db._internal_storage_try_get(key)

    def delete(self, key: storage.StorageKey) -> None:
        """
        Remove a key/value pair from storage

        Args:
            key: identifier to locate value.
        """
        self._db._internal_storage_delete(key)

    def all(self, contract_script_hash: types.UInt160 = None) -> Iterator[Tuple[storage.StorageKey,
                                                                                storage.StorageItem]]:
        """
        Retrieve all storage key/value pairs.

        Args:
            contract_script_hash: smart contract script hash to limit results to. If not specified, returns for all
            contracts.
        """
        for k, v in self._db._internal_storage_all(contract_script_hash):
            yield k, v

    def find(self, contract_script_hash: types.UInt160, key_prefix: bytes) -> Iterator[Tuple[storage.StorageKey,
                                                                                             storage.StorageItem]]:
        """
        Retrieve all storage key/value pairs.

        Args:
            contract_script_hash: script hash of smart contract to search storage of.
            key_prefix: the prefix part of the storage.StorageKey.key to look for.

        """
        for k, v in self._db._internal_storage_find(contract_script_hash, key_prefix):
            yield k, v


class RawTXAccess:
    def __init__(self, db: IDBImplementation):
        self._db = db

    def put(self, tx: payloads.Transaction) -> None:
        """
        Store a transaction.

        Args:
            tx: instance.
        """
        self._db._internal_transaction_put(tx)

    def get(self, hash: types.UInt256) -> payloads.Transaction:
        """
        Retrieve a transaction.

        Args:
            hash: transaction hash.

        Raises:
            KeyError: if the item is not found.
        """
        return self._db._internal_transaction_get(hash)

    def try_get(self, hash: types.UInt256) -> Optional[payloads.Transaction]:
        """
        Try to retrieve a transaction.

        Args:
            hash: transaction hash.
        """
        return self._db._internal_transaction_try_get(hash)

    def delete(self, hash: types.UInt256) -> None:
        """
        Remove a transaction.

        Args:
            hash: transaction hash.
        """
        self._db._internal_transaction_delete(hash)

    def all(self) -> Iterator[payloads.Transaction]:
        """
        Retrieve all stored transactions.
        """
        for tx in self._db._internal_transaction_all():
            yield tx
