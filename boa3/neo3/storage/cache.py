from __future__ import annotations

import abc
from contextlib import suppress
from copy import deepcopy
from enum import Enum, auto
from typing import Optional, Iterator, Tuple, TypeVar, Any

from boa3.neo3 import storage
from boa3.neo3.core import types
from boa3.neo3.network import payloads

TKey = TypeVar('TKey', bound='serialization.ISerializable')
TValue = TypeVar('TValue', bound='serialization.ISerializable')


class TrackState(Enum):
    NONE = auto()
    ADDED = auto()
    CHANGED = auto()
    DELETED = auto()


class Trackable:
    def __init__(self, key: TKey, value: TValue, state: TrackState):
        self.key = key
        self.item = value
        self.state = state


class CachedAccess:
    def __init__(self, db):
        self._dictionary = {}
        self._db = db
        self._internal_get = None
        self._internal_try_get = None
        self._internal_all = None

    def __getitem__(self, key):
        trackable = self._dictionary.get(key, None)  # type: Trackable
        if trackable is not None:
            if trackable.state == TrackState.DELETED:
                raise KeyError
        else:
            trackable = Trackable(key, self._internal_get(key), TrackState.NONE)
            self._dictionary.update({key: trackable})
        return trackable.item

    def _put(self, key, value):
        trackable = self._dictionary.get(key, None)  # type: Trackable
        if trackable is not None:
            if trackable.state != TrackState.DELETED:
                raise ValueError("Value already exists")
        else:
            if self._internal_try_get(key) is not None:
                raise ValueError("Value already exists")

        if trackable is None:
            trackable = Trackable(key, value, TrackState.ADDED)
        else:
            trackable = Trackable(key, value, TrackState.CHANGED)

        self._dictionary.update({key: trackable})

    def _get(self, key, read_only=False):
        """
        Return the value stored with `key`.

        Args:
            key: the identifier that can be used to retrieve the stored value
            read_only:

        Raises:
            KeyError if the key is not found.
        """
        value = self[key]
        if value is None:
            raise KeyError

        if read_only:
            # make sure that even trackables in ADDED/CHANGED state can't be modified
            return deepcopy(value)

        if self._dictionary[key].state == TrackState.NONE:
            self._dictionary[key].state = TrackState.CHANGED
        return value

    def _delete(self, key) -> None:
        """
        Delete the value stored under `key`.

        Args:
            key: the identifier that can be used to identify the stored value
        """
        trackable = self._dictionary.get(key, None)  # type: Trackable
        if trackable is not None:
            if trackable.state == TrackState.ADDED:
                self._dictionary.pop(key)
            else:
                trackable.state = TrackState.DELETED
        else:
            item = self._internal_try_get(key)
            if item is None:
                return

            self._dictionary.update({key: Trackable(key, item, TrackState.DELETED)})

    @abc.abstractmethod
    def commit(self):
        """ Persist changes"""

    @abc.abstractmethod
    def create_snapshot(self):
        """ Deep copy. """


class AttributeCache:
    def __init__(self):
        self._item = None
        self._state = TrackState.NONE

    def put(self, item) -> None:
        self._item = item

    def get(self, read_only=False) -> Any:
        if self._item is None:
            self._item = self._get_internal()

        if read_only:
            return deepcopy(self._item)
        else:
            self._state = TrackState.CHANGED
            return self._item

    def commit(self) -> None:
        if self._state == TrackState.CHANGED:
            self._update_internal(self._item)

    def create_snapshot(self) -> CloneAttributeCache:
        return CloneAttributeCache(self)

    @abc.abstractmethod
    def _get_internal(self):
        """ Return the value from the real backend. """

    @abc.abstractmethod
    def _update_internal(self, value):
        """ Update the value in the real backend. """


class CachedBlockAccess(CachedAccess):
    def __init__(self, db):
        super(CachedBlockAccess, self).__init__(db)
        self._height_hash_mapping = {}
        self._internal_get = self._db._internal_block_get
        self._internal_try_get = self._db._internal_block_try_get
        self._internal_all = self._db._internal_block_all

    def put(self, block: payloads.Block) -> None:
        """
        Store a block.

        Args:
            block: instance.

        Raises:
            ValueError: if a duplicate item is found.
        """
        block_hash = block.hash()
        super(CachedBlockAccess, self)._put(block_hash, block)
        self._height_hash_mapping.update({block.index: block_hash})

    def get(self, hash: types.UInt256, read_only=False) -> payloads.Block:
        """
        Retrieve a block.

        Args:
            hash: block hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.

        Raises:
            KeyError: if the item is not found.
        """
        block = super(CachedBlockAccess, self)._get(hash, read_only)
        self._height_hash_mapping.update({block.index: block.hash()})
        return block

    def get_by_height(self, height: int, read_only=False) -> payloads.Block:
        """
        Retrieve a block by its height.

        Args:
            height: target block index/height.
            read_only: set to True to safeguard against return value modifications being persisted when committing.

        Raises:
            KeyError: if the item is not found.
        """
        block_hash = self._height_hash_mapping.get(height, None)
        if block_hash is None:
            raise KeyError
        return self.get(block_hash, read_only)

    def try_get(self, hash: types.UInt256, read_only=False) -> Optional[payloads.Block]:
        """
        Try to retrieve a block.

        Args:
            hash: block hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        try:
            return self.get(hash, read_only)
        except KeyError:
            return None

    def try_get_by_height(self, height, read_only=False) -> Optional[payloads.Block]:
        """
        Try to retrieve a block.

        Args:
            hash: block hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        block_hash = self._height_hash_mapping.get(height, None)
        if block_hash is None:
            return None

        return self.try_get(block_hash, read_only)

    def delete(self, hash: types.UInt256) -> None:
        """
        Remove a block.

        Args:
            hash: block hash.
        """
        super(CachedBlockAccess, self)._delete(hash)
        with suppress(KeyError):
            self._height_hash_mapping.pop(hash)

    def all(self) -> Iterator[payloads.Block]:
        """
        Retrieve all blocks (readonly)
        """
        blocks = []
        for block in self._internal_all():
            if block.hash() not in self._dictionary:
                blocks.append(block)

        for k, v in self._dictionary.items():
            if v.state != TrackState.DELETED:
                blocks.append(deepcopy(v.item))

        blocks.sort(key=lambda block: block.hash().to_array())
        for block in blocks:
            yield block
        return None


class CachedContractAccess(CachedAccess):
    def __init__(self, db):
        super(CachedContractAccess, self).__init__(db)
        self._internal_get = self._db._internal_contract_get
        self._internal_try_get = self._db._internal_contract_try_get
        self._internal_all = self._db._internal_contract_all

    def put(self, contract: storage.ContractState) -> None:
        """
        Store a contract.

        Args:
            contract: contract state instance.

        Raises:
            ValueError: if a duplicate item is found.
        """
        super(CachedContractAccess, self)._put(contract.script_hash(), contract)

    def get(self, script_hash: types.UInt160, read_only=False) -> storage.ContractState:
        """
        Retrieve a contract.

        Args:
            script_hash: contract script hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.

        Raises:
            KeyError: if the item is not found.
        """
        return super(CachedContractAccess, self)._get(script_hash, read_only)

    def try_get(self, script_hash: types.UInt160, read_only=False) -> Optional[storage.ContractState]:
        """
        Try to retrieve a contract.

        Args:
            script_hash: contract script hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        try:
            return self.get(script_hash, read_only)
        except KeyError:
            return None

    def delete(self, script_hash: types.UInt160) -> None:
        """
        Remove a transaction.

        Args:
            script_hash: contract script hash.
        """
        super(CachedContractAccess, self)._delete(script_hash)

    def all(self) -> Iterator[storage.ContractState]:
        """
        Retrieve all contracts (readonly)
        """
        contracts = []
        for contract in self._internal_all():
            if contract.script_hash() not in self._dictionary:
                contracts.append(contract)

        for k, v in self._dictionary.items():
            if v.state != TrackState.DELETED:
                contracts.append(deepcopy(v.item))

        contracts.sort(key=lambda contract: contract.script_hash().to_array())
        for contract in contracts:
            yield contract
        return None


class CachedStorageAccess(CachedAccess):
    def __init__(self, db):
        super(CachedStorageAccess, self).__init__(db)
        self._internal_get = self._db._internal_storage_get
        self._internal_try_get = self._db._internal_storage_try_get
        self._internal_all = self._db._internal_storage_all
        self._internal_find = self._db._internal_storage_find

    def put(self, key: storage.StorageKey, value: storage.StorageItem) -> None:
        """
        Store the value under the given key.

        Args:
            key: identifier to store the value under.
            value: the value to be persisted.
        """
        super(CachedStorageAccess, self)._put(key, value)

    def get(self, key: storage.StorageKey, read_only=False) -> storage.StorageItem:
        """
        Retrieve a value from storage.

        Args:
            key: identifier.
            read_only: set to True to safeguard against return value modifications being persisted when committing.

        Raises:
            KeyError: if the item is not found.
        """
        return super(CachedStorageAccess, self)._get(key, read_only)

    def try_get(self, key: storage.StorageKey, read_only=False) -> Optional[storage.StorageItem]:
        """
        Try to retrieve a value from storage.

        Args:
            key: identifier.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        try:
            return self.get(key, read_only)
        except KeyError:
            return None

    def delete(self, key: storage.StorageKey) -> None:
        """
        Remove a key/value pair from storage

        Args:
            key: identifier to locate value.
        """
        super(CachedStorageAccess, self)._delete(key)

    def all(self, contract_script_hash: types.UInt160 = None) -> Iterator[Tuple[storage.StorageKey,
                                                                                storage.StorageItem]]:
        """
        Retrieve all storage key/value pairs, sorted by key (readonly).

        Note:
            Return values are sorted to give deterministic behaviour in smart contracts.

        Args:
            contract_script_hash: smart contract script hash to limit results to. If not specified, returns for all
            contracts.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        pairs = []
        for k, v in self._internal_all(contract_script_hash):
            if k not in self._dictionary:
                pairs.append((k, v))

        for k, v in self._dictionary.items():
            if v.state != TrackState.DELETED:
                pairs.append((deepcopy(v.key), deepcopy(v.item)))

        pairs.sort(key=lambda keypair: keypair[0].to_array())
        for pair in pairs:
            yield pair
        return None

    def find(self, contract_script_hash: types.UInt160, key_prefix: bytes) -> Iterator[Tuple[storage.StorageKey,
                                                                                             storage.StorageItem]]:
        """
        Retrieve all storage key/value pairs (readonly).

        Args:
            contract_script_hash: script hash of smart contract to search storage of.
            key_prefix: the prefix part of the storage.StorageKey.key to look for.

        """
        pairs = []
        for k, v in self._internal_find(contract_script_hash, key_prefix):
            if k not in self._dictionary:
                pairs.append((k, v))

        for k, v in self._dictionary.items():
            if v.state != TrackState.DELETED and k.key.startswith(key_prefix):
                pairs.append((deepcopy(v.key), deepcopy(v.item)))

        pairs.sort(key=lambda keypair: keypair[0].to_array())
        for pair in pairs:
            yield pair
        return None


class CachedTXAccess(CachedAccess):
    def __init__(self, db):
        super(CachedTXAccess, self).__init__(db)
        self._internal_get = self._db._internal_transaction_get
        self._internal_try_get = self._db._internal_transaction_try_get
        self._internal_all = self._db._internal_transaction_all

    def put(self, tx: payloads.Transaction) -> None:
        """
        Store a transaction.

        Args:
            tx: instance.

        Raises:
            ValueError: if a duplicate item is found.
        """
        super(CachedTXAccess, self)._put(tx.hash(), tx)

    def get(self, hash: types.UInt256, read_only=False) -> payloads.Transaction:
        """
        Retrieve a transaction.

        Args:
            hash: transaction hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.

        Raises:
            KeyError: if the item is not found.
        """
        return super(CachedTXAccess, self)._get(hash, read_only)

    def try_get(self, hash: types.UInt256, read_only=False) -> Optional[payloads.Transaction]:
        """
        Try to retrieve a transaction.

        Args:
            hash: transaction hash.
            read_only: set to True to safeguard against return value modifications being persisted when committing.
        """
        try:
            return self.get(hash, read_only)
        except KeyError:
            return None

    def delete(self, hash: types.UInt256) -> None:
        """
        Remove a transaction.

        Args:
            hash: transaction hash.
        """
        super(CachedTXAccess, self)._delete(hash)

    def all(self) -> Iterator[payloads.Transaction]:
        """
        Retrieve all transactions (readonly)
        """
        transactions = []
        for tx in self._internal_all():
            if tx.hash() not in self._dictionary:
                transactions.append(tx)

        for k, v in self._dictionary.items():
            if v.state != TrackState.DELETED:
                transactions.append(deepcopy(v.item))

        transactions.sort(key=lambda tx: tx.hash().to_array())
        for tx in transactions:
            yield tx
        return None


"""
Yes there is near duplicate code for all the Clone_xxx_Cache classes. 

A solution with a generic CloneCache and multiple inheritance quickly became hard to follow in part because Python 
requires all parent classes to be designed for multiple inheritance (where our case needs different super args). The 
solution using **kwargs in combination with no manual controllable MRO becomes a mess. 

Revisit later when there's more time to think about the problem again. 
"""


class CloneBlockCache(CachedBlockAccess):
    def __init__(self, db, inner_cache: CachedBlockAccess):
        super(CloneBlockCache, self).__init__(db)
        self.inner_cache = inner_cache
        self._internal_get = self._inner_cache_get
        self._internal_try_get = self._inner_cache_try_get
        self._internal_all = self._inner_cache_all

    def _inner_cache_try_get(self, hash, read_only=True):
        try:
            return self._inner_cache_get(hash, read_only)
        except KeyError:
            return None

    def _inner_cache_get(self, hash, read_only=True):
        return self.inner_cache.get(hash, read_only)

    def _inner_cache_all(self):
        return self.inner_cache.all()

    def commit(self) -> None:
        """
        Persist changes to the parent snapshot.
        """
        for trackable in self._dictionary.values():  # trackable.item: payloads.Block
            if trackable.state == TrackState.ADDED:
                self.inner_cache.put(trackable.item)
            elif trackable.state == TrackState.CHANGED:
                # This one is kind of useless unless we augment Block with additional attributes (like done with
                # Transaction) and the IDBImplementation class calls are updated to serialize_special(). Otherwise, any
                # attribute changes will modify the hash of the Block causing it to not be found.
                item = self.inner_cache.try_get(trackable.item.hash(), read_only=False)
                if item:
                    item.from_replica(trackable.item)
            elif trackable.state == TrackState.DELETED:
                self.inner_cache.delete(trackable.item.hash())


class CloneContractCache(CachedContractAccess):
    def __init__(self, db, inner_cache: CachedContractAccess):
        super(CloneContractCache, self).__init__(db)
        self.inner_cache = inner_cache
        self._internal_get = self._inner_cache_get
        self._internal_try_get = self._inner_cache_try_get
        self._internal_all = self._inner_cache_all

    def _inner_cache_try_get(self, hash, read_only=True):
        try:
            return self._inner_cache_get(hash, read_only)
        except KeyError:
            return None

    def _inner_cache_get(self, hash, read_only=True):
        return self.inner_cache.get(hash, read_only)

    def _inner_cache_all(self):
        return self.inner_cache.all()

    def commit(self) -> None:
        """
        Persist changes to the parent snapshot.
        """
        for trackable in self._dictionary.values():  # trackable.item: storage.ContractState
            if trackable.state == TrackState.ADDED:
                self.inner_cache.put(trackable.item)
            elif trackable.state == TrackState.CHANGED:
                item = self.inner_cache.try_get(trackable.item.script_hash(), read_only=False)
                if item:
                    item.from_replica(trackable.item)
            elif trackable.state == TrackState.DELETED:
                self.inner_cache.delete(trackable.item.script_hash())


class CloneStorageCache(CachedStorageAccess):
    def __init__(self, db, inner_cache: CachedStorageAccess):
        super(CloneStorageCache, self).__init__(db)
        self.inner_cache = inner_cache
        self._internal_get = self._inner_cache_get
        self._internal_try_get = self._inner_cache_try_get
        self._internal_all = self._inner_cache_all
        self._internal_find = self._inner_cache_find

    def _inner_cache_try_get(self, hash, read_only=True):
        try:
            return self._inner_cache_get(hash, read_only)
        except KeyError:
            return None

    def _inner_cache_get(self, hash, read_only=True):
        return self.inner_cache.get(hash, read_only)

    def _inner_cache_all(self, contract_script_hash):
        return self.inner_cache.all(contract_script_hash)

    def _inner_cache_find(self, contract_script_hash, key_prefix):
        return self.inner_cache.find(contract_script_hash, key_prefix)

    def commit(self) -> None:
        """
        Persist changes to the parent snapshot.
        """
        for trackable in self._dictionary.values():
            if trackable.state == TrackState.ADDED:
                self.inner_cache.put(trackable.key, trackable.item)
            elif trackable.state == TrackState.CHANGED:
                item = self.inner_cache.try_get(trackable.key, read_only=False)
                if item:
                    item.from_replica(trackable.item)
            elif trackable.state == TrackState.DELETED:
                self.inner_cache.delete(trackable.key)


class CloneTXCache(CachedTXAccess):
    def __init__(self, db, inner_cache: CachedTXAccess):
        super(CloneTXCache, self).__init__(db)
        self.inner_cache = inner_cache
        self._internal_get = self._inner_cache_get
        self._internal_try_get = self._inner_cache_try_get
        self._internal_all = self._inner_cache_all

    def _inner_cache_try_get(self, hash, read_only=True):
        try:
            return self._inner_cache_get(hash, read_only)
        except KeyError:
            return None

    def _inner_cache_get(self, hash, read_only=True):
        return self.inner_cache.get(hash, read_only)

    def _inner_cache_all(self):
        return self.inner_cache.all()

    def commit(self) -> None:
        """
        Persist changes to the parent snapshot.
        """
        for trackable in self._dictionary.values():  # trackable.item: payloads.Transaction
            if trackable.state == TrackState.ADDED:
                self.inner_cache.put(trackable.item)
            elif trackable.state == TrackState.CHANGED:
                # Note that any changes to TX attributes that are serialized changes the hash and thus we won't find it
                # anymore in the cache.
                #
                # This means the changes will be persisted in the DB with a new entry!
                # We can however augment the TX class with e.g. VMState and BlockIndex without affecting the hash.
                # For all other cases the behaviour of a `transaction.get(hash)` is equal to
                # `transaction.get(hash, readonly=True) as no data will be persisted.
                item = self.inner_cache.try_get(trackable.item.hash(), read_only=False)
                if item:
                    item.from_replica(trackable.item)
            elif trackable.state == TrackState.DELETED:
                self.inner_cache.delete(trackable.item.hash())


class CloneAttributeCache(AttributeCache):
    def __init__(self, inner_cache: AttributeCache):
        super(CloneAttributeCache, self).__init__()
        self._inner_cache = inner_cache

    def _get_internal(self):
        return self._inner_cache.get()

    def _update_internal(self, value):
        self._inner_cache.put(value)
