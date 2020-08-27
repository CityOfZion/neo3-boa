from __future__ import annotations

from contextlib import suppress
from copy import deepcopy
from typing import Iterator, Tuple, Dict

from boa3.neo3 import storage
from boa3.neo3.core import types
from boa3.neo3.network import payloads


class MemoryDB(storage.IDBImplementation):
    BLOCK = 'blocks'
    BLOCK_HEIGHT_MAP = 'blocksmap'
    BLOCK_BEST_HEIGHT = 'blockheight'
    CONTRACT = 'contracts'
    STORAGE = 'storages'
    TX = 'transactions'

    def __init__(self, options: dict = None):
        self.db: Dict[str, dict] = {
            self.BLOCK: {},
            self.BLOCK_HEIGHT_MAP: {},
            self.CONTRACT: {},
            self.STORAGE: {},
            self.TX: {}
        }
        self._best_block_height = -1

    def get_snapshotview(self) -> MemorySnapshot:
        return MemorySnapshot(self)

    def _internal_bestblockheight_get(self):
        if self._best_block_height == -1:
            raise KeyError
        return self._best_block_height

    def _internal_bestblockheight_put(self, height: int, batch=None):
        if batch:
            batch.put(self.BLOCK_BEST_HEIGHT, height, height)
        else:
            self._best_block_height = height

    def _internal_bestblockheight_update(self, height: int, batch=None):
        self._internal_bestblockheight_put(height, batch)

    def _internal_block_put(self, block: payloads.Block, batch: WriteBatch = None) -> None:
        if batch:
            batch.put(self.BLOCK, block.hash(), block)
        else:
            self.db[self.BLOCK][block.hash()] = block
            self.db[self.BLOCK_HEIGHT_MAP][block.index] = block.hash()

        stored_value = -1
        with suppress(KeyError):
            stored_value = self._internal_bestblockheight_get()

        if block.index > stored_value:
            self._best_block_height = block.index

    def _internal_block_update(self, block: payloads.Block, batch: WriteBatch = None) -> None:
        self._internal_block_put(block, batch)

    def _internal_block_delete(self, hash: types.UInt256, batch: WriteBatch = None) -> None:
        if batch:
            batch.delete(self.BLOCK, hash)
        else:
            with suppress(KeyError):
                block = self.db[self.BLOCK].pop(hash)
                self.db[self.BLOCK_HEIGHT_MAP].pop(block.index)

    def _internal_block_get(self, hash: types.UInt256) -> payloads.Block:
        value = self.db[self.BLOCK].get(hash, None)
        if value is None:
            raise KeyError
        return deepcopy(value)

    def _internal_block_get_by_height(self, height: int) -> payloads.Block:
        block_hash = self.db[self.BLOCK_HEIGHT_MAP].get(height, None)
        if block_hash is None:
            raise KeyError

        return self._internal_block_get(block_hash)

    def _internal_block_all(self) -> Iterator[payloads.Block]:
        for block in self.db[self.BLOCK].values():
            yield deepcopy(block)

    def _internal_contract_put(self, contract: storage.ContractState, batch: WriteBatch = None) -> None:
        if batch:
            batch.put(self.CONTRACT, contract.script_hash(), contract)
        else:
            self.db[self.CONTRACT][contract.script_hash()] = contract

    def _internal_contract_update(self, contract: storage.ContractState, batch: WriteBatch = None) -> None:
        self._internal_contract_put(contract, batch)

    def _internal_contract_delete(self, script_hash: types.UInt160, batch: WriteBatch = None) -> None:
        if batch:
            batch.delete(self.CONTRACT, script_hash)
        else:
            with suppress(KeyError):
                self.db[self.CONTRACT].pop(script_hash)

    def _internal_contract_get(self, script_hash: types.UInt160) -> storage.ContractState:
        value = self.db[self.CONTRACT].get(script_hash, None)
        if value is None:
            raise KeyError

        return deepcopy(value)

    def _internal_contract_all(self) -> Iterator[storage.ContractState]:
        for contract in self.db[self.CONTRACT].values():
            yield deepcopy(contract)

    def _internal_storage_put(self, key: storage.StorageKey,
                              value: storage.StorageItem,
                              batch: WriteBatch = None) -> None:
        if batch:
            batch.put(self.STORAGE, key, value)
        else:
            self.db[self.STORAGE][key] = value

    def _internal_storage_update(self, key: storage.StorageKey,
                                 value: storage.StorageItem,
                                 batch: WriteBatch = None) -> None:
        self._internal_storage_put(key, value, batch)

    def _internal_storage_delete(self, key: storage.StorageKey, batch: WriteBatch = None) -> None:
        if batch:
            batch.delete(self.STORAGE, key)
        else:
            with suppress(KeyError):
                self.db[self.STORAGE].pop(key)

    def _internal_storage_get(self, key: storage.StorageKey) -> storage.StorageItem:
        value = self.db[self.STORAGE].get(key, None)
        if value is None:
            raise KeyError

        return deepcopy(value)

    def _internal_storage_all(self, contract_script_hash: types.UInt160 = None) -> Iterator[Tuple[storage.StorageKey,
                                                                                                  storage.StorageItem]]:
        for k, v in self.db[self.STORAGE].items():
            if contract_script_hash:
                if contract_script_hash == k.contract:
                    yield deepcopy(k), deepcopy(v)
            else:
                yield deepcopy(k), deepcopy(v)

    def _internal_storage_find(self, contract_script_hash: types.UInt160,
                               key_prefix: bytes) -> Iterator[Tuple[storage.StorageKey, storage.StorageItem]]:
        script_hash_len = 20
        for k, v in self.db[self.STORAGE].items():
            # k is of type StorageKey, which starts with a 20-byte script hash.
            # We skip this and search only in the `key` attribute
            if k.to_array()[script_hash_len:].startswith(key_prefix):
                yield deepcopy(k), deepcopy(v)

    def _internal_transaction_put(self, transaction: payloads.Transaction, batch: WriteBatch = None) -> None:
        if batch:
            batch.put(self.TX, transaction.hash(), transaction)
        else:
            self.db[self.TX][transaction.hash()] = transaction

    def _internal_transaction_update(self, transaction: payloads.Transaction, batch: WriteBatch = None) -> None:
        self._internal_transaction_put(transaction, batch)

    def _internal_transaction_delete(self, hash: types.UInt256, batch: WriteBatch = None) -> None:
        if batch:
            batch.delete(self.TX, hash)
        else:
            with suppress(KeyError):
                self.db[self.TX].pop(hash)

    def _internal_transaction_get(self, hash: types.UInt256) -> payloads.Transaction:
        value = self.db[self.TX].get(hash, None)
        if value is None:
            raise KeyError

        return deepcopy(value)

    def _internal_transaction_all(self) -> Iterator[payloads.Transaction]:
        for tx in self.db[self.TX].values():
            yield deepcopy(tx)

    def write_batch(self, batch) -> None:
        for table, action, pair in batch:
            if action == 'delete':
                item = self.db[table].pop(pair[0])
                if table == self.BLOCK:
                    self.db[self.BLOCK_HEIGHT_MAP].pop(item.index)
            elif action in ['update', 'add']:
                if table == self.BLOCK_BEST_HEIGHT:
                    self._best_block_height = pair[0]
                    continue
                self.db[table][pair[0]] = pair[1]
                if table == self.BLOCK:
                    # pair = (UInt256, Block)
                    self.db[self.BLOCK_HEIGHT_MAP][pair[1].index] = pair[0]


class WriteBatch:
    def __init__(self):
        self.statements = []

    def __iter__(self):
        for s in self.statements:
            yield s

    def put(self, table, key, value) -> None:
        self.statements.append((table, 'add', (key, value)))

    def delete(self, table, key) -> None:
        self.statements.append((table, 'delete', (key, None)))


class MemorySnapshot(storage.Snapshot):
    def __init__(self, db: MemoryDB):
        super(MemorySnapshot, self).__init__()
        self._db = db
        self._batch = WriteBatch()

        self._block_cache = MemoryDBCachedBlockAccess(db, self._batch)
        self._contract_cache = MemoryDBCachedContractAccess(db, self._batch)
        self._storage_cache = MemoryDBCachedStorageAccess(db, self._batch)
        self._tx_cache = MemoryDBCachedTXAccess(db, self._batch)
        self._block_height_cache = MemoryBestBlockHeightAttribute(db, self._batch)

    def commit(self) -> None:
        super(MemorySnapshot, self).commit()
        self._db.write_batch(self._batch)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # nothing to do
        pass


class MemoryBestBlockHeightAttribute(storage.AttributeCache):
    def __init__(self, db, batch):
        super(MemoryBestBlockHeightAttribute, self).__init__()
        self._db = db
        self._batch = batch

    def _get_internal(self):
        return self._db._internal_bestblockheight_get()

    def _update_internal(self, value):
        self._db._internal_bestblockheight_update(value, self._batch)


class MemoryDBCachedBlockAccess(storage.CachedBlockAccess):
    def __init__(self, db, batch):
        super(MemoryDBCachedBlockAccess, self).__init__(db)
        self._batch = batch

    def commit(self) -> None:
        for trackable in self._dictionary.values():  # trackable.item: payloads.Block
            if trackable.state == storage.TrackState.ADDED:
                self._db._internal_block_put(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.CHANGED:
                self._db._internal_block_update(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.DELETED:
                self._db._internal_block_delete(trackable.item.hash(), self._batch)

    def create_snapshot(self):
        return storage.CloneBlockCache(self._db, self)


class MemoryDBCachedContractAccess(storage.CachedContractAccess):
    def __init__(self, db, batch):
        super(MemoryDBCachedContractAccess, self).__init__(db)
        self._batch = batch

    def commit(self) -> None:
        for trackable in self._dictionary.values():  # trackable.item: storage.ContractState
            if trackable.state == storage.TrackState.ADDED:
                self._db._internal_contract_put(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.CHANGED:
                self._db._internal_contract_update(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.DELETED:
                self._db._internal_contract_delete(trackable.item.script_hash(), self._batch)

    def create_snapshot(self):
        return storage.CloneContractCache(self._db, self)


class MemoryDBCachedStorageAccess(storage.CachedStorageAccess):
    def __init__(self, db, batch):
        super(MemoryDBCachedStorageAccess, self).__init__(db)
        self._batch = batch

    def commit(self) -> None:
        for trackable in self._dictionary.values():
            if trackable.state == storage.TrackState.ADDED:
                self._db._internal_storage_put(trackable.key, trackable.item, self._batch)
            elif trackable.state == storage.TrackState.CHANGED:
                self._db._internal_storage_update(trackable.key, trackable.item, self._batch)
            elif trackable.state == storage.TrackState.DELETED:
                self._db._internal_storage_delete(trackable.key, self._batch)

    def create_snapshot(self):
        return storage.CloneStorageCache(self._db, self)


class MemoryDBCachedTXAccess(storage.CachedTXAccess):
    def __init__(self, db, batch):
        super(MemoryDBCachedTXAccess, self).__init__(db)
        self._batch = batch

    def commit(self) -> None:
        for trackable in self._dictionary.values():  # trackable.item: payloads.Transaction
            if trackable.state == storage.TrackState.ADDED:
                self._db._internal_transaction_put(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.CHANGED:
                self._db._internal_transaction_update(trackable.item, self._batch)
            elif trackable.state == storage.TrackState.DELETED:
                self._db._internal_transaction_delete(trackable.item.hash(), self._batch)

    def create_snapshot(self):
        return storage.CloneTXCache(self._db, self)
