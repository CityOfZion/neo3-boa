from __future__ import annotations

from contextlib import suppress
from copy import deepcopy

from boa3.neo3 import storage
from boa3.neo3 import storage_logger as logger
from boa3.neo3.core import types, serialization
from boa3.neo3.network import payloads

level_db_supported = False
with suppress(ModuleNotFoundError):
    import plyvel  # type: ignore
    level_db_supported = True


class DBPrefixes:
    BLOCKS = b'\x01'
    BLOCKS_HEIGHT_MAP = b'\x02'
    BLOCKS_BEST_HEIGHT = b'\x03'
    CONTRACTS = b'\x04'
    STORAGES = b'\x05'
    TRANSACTIONS = b'\x06'


class LevelDB(storage.IDBImplementation):
    def __init__(self, options: dict):
        if not level_db_supported:
            raise ModuleNotFoundError("plyvel module not found - try 'pip install plyvel'. "
                                      "Also make sure to have leveldb installed.")
        try:
            self._path = options['path']
            self._real_db = plyvel.DB(self._path, create_if_missing=True, max_open_files=100,
                                      lru_cache_size=10 * 1024 * 1024)
            self._tx_iterator = None
            self._block_iterator = None
            self._contract_iterator = None
            logger.info(f"Created DB at {self._path}")
        except Exception as e:
            raise Exception(f"leveldb exception [ {e} ]")

    def get_snapshotview(self) -> LevelDBSnapshot:
        return LevelDBSnapshot(self)

    def _internal_bestblockheight_get(self):
        height_bytes = self._real_db.get(DBPrefixes.BLOCKS_BEST_HEIGHT)
        if height_bytes is None:
            raise KeyError
        return int.from_bytes(height_bytes, 'little')

    def _internal_bestblockheight_put(self, height: int, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        db.put(DBPrefixes.BLOCKS_BEST_HEIGHT, height.to_bytes(4, 'little'))

    def _internal_bestblockheight_update(self, height: int, batch=None):
        self._internal_bestblockheight_put(height, batch)

    def _internal_block_put(self, block: payloads.Block, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        block_height_bytes = block.index.to_bytes(4, 'little')
        db.put(DBPrefixes.BLOCKS + block.hash().to_array(), block.to_array())
        db.put(DBPrefixes.BLOCKS_HEIGHT_MAP + block_height_bytes, block.hash().to_array())

        # this function is only called when putting blocks to the backend via the raw view, or when committing
        # a snapshot view. Either way it is ok to persist the height
        stored_value = -1
        with suppress(KeyError):
            stored_value = self._internal_bestblockheight_get()

        if block.index > stored_value:
            db.put(DBPrefixes.BLOCKS_BEST_HEIGHT, block_height_bytes)

    def _internal_block_update(self, block: payloads.Block, batch=None):
        self._internal_block_put(block, batch)

    def _internal_block_delete(self, hash: types.UInt256, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        block_hash_bytes = hash.to_array()
        block_bytes = self._real_db.get(DBPrefixes.BLOCKS + block_hash_bytes)
        if block_bytes is not None:
            # Instead of full block deserialization, which includes merkletree calculation and such, we manually extract
            # the 4 bytes block.index from the stream.
            start_idx = 4 + 32 + 32 + 8
            block_height_bytes = block_bytes[start_idx:start_idx + 4]
            db.delete(DBPrefixes.BLOCKS + block_hash_bytes)
            db.delete(DBPrefixes.BLOCKS_HEIGHT_MAP + block_height_bytes)

    def _internal_block_get(self, hash: types.UInt256):
        block_bytes = self._real_db.get(DBPrefixes.BLOCKS + hash.to_array())
        if block_bytes is None:
            raise KeyError

        return payloads.Block.deserialize_from_bytes(block_bytes)

    def _internal_block_get_by_height(self, height: int):
        block_hash_bytes = self._real_db.get(DBPrefixes.BLOCKS_HEIGHT_MAP + height.to_bytes(4, 'little'))
        if block_hash_bytes is None:
            raise KeyError

        block_bytes = self._real_db.get(DBPrefixes.BLOCKS + block_hash_bytes)
        if block_bytes is None:
            # should not be reachable unless _internal_block_put/delete() are messed up.
            raise KeyError  # pragma: no cover

        return payloads.Block.deserialize_from_bytes(block_bytes)

    def _internal_block_all(self):
        res = []

        with self._real_db.iterator(prefix=DBPrefixes.BLOCKS, include_key=False, include_value=True) as it:
            for value in it:
                v = payloads.Block.deserialize_from_bytes(value)
                res.append(v)

            # yielding outside of iterator to make sure the LevelDB iterator is closed and not leaking resources
            for block in res:
                yield deepcopy(block)

    def _internal_contract_put(self, contract: storage.ContractState, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        db.put(DBPrefixes.CONTRACTS + contract.script_hash().to_array(), contract.to_array())

    def _internal_contract_update(self, contract: storage.ContractState, batch=None):
        self._internal_contract_put(contract, batch)

    def _internal_contract_delete(self, script_hash: types.UInt160, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        db.delete(DBPrefixes.CONTRACTS + script_hash.to_array())

    def _internal_contract_get(self, script_hash: types.UInt160):
        contract_bytes = self._real_db.get(DBPrefixes.CONTRACTS + script_hash.to_array())
        if contract_bytes is None:
            raise KeyError

        return storage.ContractState.deserialize_from_bytes(contract_bytes)

    def _internal_contract_all(self):
        res = []
        with self._real_db.iterator(prefix=DBPrefixes.CONTRACTS, include_key=False, include_value=True) as it:
            for value in it:
                # strip off prefix
                v = storage.ContractState.deserialize_from_bytes(value)
                res.append(v)

        # yielding outside of iterator to make sure the LevelDB iterator is closed and not leaking resources
        for contract in res:
            yield deepcopy(contract)

    def _internal_storage_put(self, key: storage.StorageKey, value: storage.StorageItem, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        db.put(DBPrefixes.STORAGES + key.to_array(), value.to_array())

    def _internal_storage_update(self, key: storage.StorageKey, value: storage.StorageItem, batch=None):
        self._internal_storage_put(key, value)

    def _internal_storage_delete(self, key: storage.StorageKey, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        db.delete(DBPrefixes.STORAGES + key.to_array())

    def _internal_storage_get(self, key: storage.StorageKey):
        storage_bytes = self._real_db.get(DBPrefixes.STORAGES + key.to_array())
        if storage_bytes is None:
            raise KeyError

        return storage.StorageItem.deserialize_from_bytes(storage_bytes)

    def _internal_storage_all(self, contract_script_hash: types.UInt160 = None):
        prefix = DBPrefixes.STORAGES
        if contract_script_hash is not None:
            prefix = DBPrefixes.STORAGES + contract_script_hash.to_array()

        res = {}
        with self._real_db.iterator(prefix=prefix, include_key=True, include_value=True) as it:
            for key, value in it:
                # strip off prefix
                k = storage.StorageKey.deserialize_from_bytes(key[1:])
                v = storage.StorageItem.deserialize_from_bytes(value)
                res[k] = v

        # yielding outside of iterator to make sure the LevelDB iterator is closed and not leaking resources
        for k, v in res.items():
            yield deepcopy(k), deepcopy(v)

    def _internal_storage_find(self, contract_script_hash: types.UInt160, key_prefix: bytes):
        prefix = DBPrefixes.STORAGES + contract_script_hash.to_array() + key_prefix

        res = {}
        with self._real_db.iterator(prefix=prefix, include_key=True, include_value=True) as it:
            for key, value in it:
                # strip off prefix
                k = storage.StorageKey.deserialize_from_bytes(key[1:])
                v = storage.StorageItem.deserialize_from_bytes(value)
                res[k] = v

        # yielding outside of iterator to make sure the LevelDB iterator is closed and not leaking resources
        for k, v in res.items():
            yield k, v

    def _internal_transaction_put(self, transaction: payloads.Transaction, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db

        with serialization.BinaryWriter() as bw:
            transaction.serialize_special(bw)
            serialized_tx = bw.to_array()

        db.put(DBPrefixes.TRANSACTIONS + transaction.hash().to_array(), serialized_tx)

    def _internal_transaction_update(self, transaction, batch=None):
        self._internal_transaction_put(transaction, batch)

    def _internal_transaction_delete(self, hash: types.UInt256, batch=None):
        if batch:
            db = batch
        else:
            db = self._real_db
        db.delete(DBPrefixes.TRANSACTIONS + hash.to_array())

    def _internal_transaction_get(self, hash: types.UInt256):
        tx_bytes = self._real_db.get(DBPrefixes.TRANSACTIONS + hash.to_array())
        if tx_bytes is None:
            # this is a must if not found!
            raise KeyError

        with serialization.BinaryReader(tx_bytes) as br:
            tx = payloads.Transaction()
            tx.deserialize_special(br)
            return tx

    def _internal_transaction_all(self):
        res = []
        with self._real_db.iterator(prefix=DBPrefixes.TRANSACTIONS, include_key=False, include_value=True) as it:
            for value in it:
                # strip off prefix
                with serialization.BinaryReader(value) as br:
                    v = payloads.Transaction()
                    v.deserialize_special(br)
                    res.append(v)

        # yielding outside of iterator to make sure the LevelDB iterator is closed and not leaking resources
        for tx in res:
            yield deepcopy(tx)

    def close(self):
        self._real_db.close()


class LevelDBSnapshot(storage.Snapshot):
    def __init__(self, db: LevelDB):
        super(LevelDBSnapshot, self).__init__()
        self._db = db
        self._snapshot = db._real_db.snapshot()
        self._batch = db._real_db.write_batch()

        self._block_cache = LevelDBCachedBlockAccess(db, self._batch)
        self._contract_cache = LevelDBCachedContractAccess(db, self._batch)
        self._storage_cache = LevelDBCachedStorageAccess(db, self._batch)
        self._tx_cache = LevelDBCachedTXAccess(db, self._batch)
        self._block_height_cache = LevelDBBestBlockHeightAttribute(db, self._batch)

    def commit(self) -> None:
        super(LevelDBSnapshot, self).commit()
        self._batch.write()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._snapshot.close()


class LevelDBBestBlockHeightAttribute(storage.AttributeCache):
    def __init__(self, db, batch):
        super(LevelDBBestBlockHeightAttribute, self).__init__()
        self._db = db
        self._batch = batch

    def _get_internal(self):
        return self._db._internal_bestblockheight_get()

    def _update_internal(self, value):
        self._db._internal_bestblockheight_update(value, self._batch)


class LevelDBCachedBlockAccess(storage.CachedBlockAccess):
    def __init__(self, db, batch):
        super(LevelDBCachedBlockAccess, self).__init__(db)
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


class LevelDBCachedContractAccess(storage.CachedContractAccess):
    def __init__(self, db, batch):
        super(LevelDBCachedContractAccess, self).__init__(db)
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


class LevelDBCachedStorageAccess(storage.CachedStorageAccess):
    def __init__(self, db, batch):
        super(LevelDBCachedStorageAccess, self).__init__(db)
        self._batch = batch

    def commit(self) -> None:
        for trackable in self._dictionary.values():  # type: storage.Trackable
            if trackable.state == storage.TrackState.ADDED:
                self._db._internal_storage_put(trackable.key, trackable.item, self._batch)
            elif trackable.state == storage.TrackState.CHANGED:
                self._db._internal_storage_update(trackable.key, trackable.item, self._batch)
            elif trackable.state == storage.TrackState.DELETED:
                self._db._internal_storage_delete(trackable.key, self._batch)

    def create_snapshot(self):
        return storage.CloneStorageCache(self._db, self)


class LevelDBCachedTXAccess(storage.CachedTXAccess):
    def __init__(self, db, batch):
        super(LevelDBCachedTXAccess, self).__init__(db)
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
