from __future__ import annotations

from boa3.neo3 import storage, settings
from boa3.neo3.network import payloads, convenience


class Blockchain(convenience._Singleton):

    def init(self, backend: storage.IDBImplementation = None):  # type: ignore
        self.backend = backend if backend else settings.database
        self._current_snapshot = None

    @property
    def currentSnapshot(self) -> storage.Snapshot:
        if self._current_snapshot is None:
            self._current_snapshot = self.backend.get_snapshotview()
        return self._current_snapshot  # type: ignore
        # mypy thinks it returns None

    @property
    def height(self):
        return self.currentSnapshot.block_height

    async def persist(self, block: payloads.Block):
        with self.backend.get_snapshotview() as snapshot:
            snapshot.block_height = block.index
            snapshot.blocks.put(block)

            for tx in block.transactions:
                tx.block_height = block.index
                snapshot.transactions.put(tx)

                # TODO: run VM

            snapshot.commit()
            self._current_snapshot = snapshot
