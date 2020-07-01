from __future__ import annotations

import abc

from boa3.neo3 import storage


class Snapshot:
    def __init__(self):
        self._block_cache: storage.CachedBlockAccess = None
        self._contract_cache: storage.CachedContractAccess = None
        self._storage_cache: storage.CachedStorageAccess = None
        self._tx_cache: storage.CachedTXAccess = None
        self._block_height_cache: storage.AttributeCache = None

    @property
    def blocks(self):
        return self._block_cache

    @property
    def contracts(self):
        return self._contract_cache

    @property
    def storages(self):
        return self._storage_cache

    @property
    def transactions(self):
        return self._tx_cache

    @property
    def block_height(self) -> int:
        try:
            return self._block_height_cache.get()
        except KeyError:
            return -1

    @block_height.setter
    def block_height(self, value) -> None:
        self._block_height_cache.put(value)

    def commit(self):
        """

        Returns:

        """
        self._block_cache.commit()
        self._contract_cache.commit()
        self._storage_cache.commit()
        self._tx_cache.commit()
        self._block_height_cache.commit()

    def clone(self) -> CloneSnapshot:
        return CloneSnapshot(self)

    @abc.abstractmethod
    def __enter__(self):
        """"""

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup resources if necessary."""


class CloneSnapshot(Snapshot):
    def __init__(self, snapshot: Snapshot):
        super(CloneSnapshot, self).__init__()
        self._snapshot = snapshot
        self._block_cache = snapshot.blocks.create_snapshot()
        self._contract_cache = snapshot.contracts.create_snapshot()
        self._storage_cache = snapshot.storages.create_snapshot()
        self._tx_cache = snapshot.transactions.create_snapshot()
        self._block_height_cache = snapshot._block_height_cache.create_snapshot()

    def commit(self):
        super(CloneSnapshot, self).commit()

    def __enter__(self):
        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
