from __future__ import annotations

import hashlib
from copy import deepcopy
from typing import List

from bitarray import bitarray  # type: ignore

from boa3.neo3.core import Size as s, serialization, types, utils, cryptography as crypto, IClonable
from boa3.neo3.network import payloads


class _BlockBase(serialization.ISerializable):
    def __init__(self,
                 version: int = 0,
                 prev_hash: types.UInt256 = None,
                 merkle_root: types.UInt256 = None,
                 timestamp: int = 0,
                 index: int = 0,
                 next_consensus: types.UInt160 = None,
                 witness: payloads.Witness = None
                 ):

        self.version = version
        self.prev_hash = prev_hash if prev_hash else types.UInt256.zero()
        self.merkle_root = merkle_root if merkle_root else types.UInt256.zero()
        self.timestamp = timestamp
        self.index = index
        self.next_consensus = next_consensus if next_consensus else types.UInt160.zero()
        self.witness = witness if witness else payloads.Witness()

    def __len__(self):
        return s.uint32 + s.uint256 + s.uint256 + s.uint64 + s.uint32 + s.uint160 + 1 + len(self.witness)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        self.serialize_unsigned(writer)
        writer.write_uint8(1)
        writer.write_serializable(self.witness)

    def serialize_unsigned(self, writer: serialization.BinaryWriter) -> None:
        writer.write_uint32(self.version)
        writer.write_serializable(self.prev_hash)
        writer.write_serializable(self.merkle_root)
        writer.write_uint64(self.timestamp)
        writer.write_uint32(self.index)
        writer.write_serializable(self.next_consensus)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.

        Raises:
            ValueError: if no witnesses are found.
        """
        self.deserialize_unsigned(reader)
        witness_obj_count = reader.read_uint8()
        if witness_obj_count != 1:
            raise ValueError(f"Deserialization error - Witness object count is {witness_obj_count} must be 1")
        self.witness = reader.read_serializable(payloads.Witness)

    def deserialize_unsigned(self, reader: serialization.BinaryReader) -> None:
        self.version = reader.read_uint32()
        self.prev_hash = reader.read_serializable(types.UInt256)
        self.merkle_root = reader.read_serializable(types.UInt256)
        self.timestamp = reader.read_uint64()
        self.index = reader.read_uint32()
        self.next_consensus = reader.read_serializable(types.UInt160)

    def hash(self) -> types.UInt256:
        """
        Get a unique block identifier based on the unsigned data portion of the object.
        """
        with serialization.BinaryWriter() as bw:
            self.serialize_unsigned(bw)
            data_to_hash = bytearray(bw._stream.getvalue())
            data = hashlib.sha256(hashlib.sha256(data_to_hash).digest()).digest()
            return types.UInt256(data=data)


class Header(_BlockBase):
    """
    A Block header only object.

    Does not contain any consensus data or transactions.

    See also:
        :class:`~neo3.network.payloads.block.TrimmedBlock`
    """

    def __init__(self,
                 version: int = 0,
                 prev_hash: types.UInt256 = None,
                 merkle_root: types.UInt256 = None,
                 timestamp: int = 0,
                 index: int = 0,
                 next_consensus: types.UInt160 = None,
                 witness: payloads.Witness = None
                 ):
        super(Header, self).__init__(version, prev_hash, merkle_root, timestamp, index, next_consensus, witness)

    def __len__(self):
        return super(Header, self).__len__() + 1

    def __eq__(self, other):
        if other is None:
            return False
        if type(self) != type(other):
            return False
        if self.hash() != other.hash():
            return False
        return True

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        super(Header, self).serialize(writer)
        writer.write_uint8(0)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.

        Raises:
            ValueError: if the check byte does not equal.
        """
        super(Header, self).deserialize(reader)
        tmp = reader.read_uint8()
        if tmp != 0:
            raise ValueError("Deserialization error")


class Block(_BlockBase, payloads.IInventory):
    """
    The famous Block. I transfer chain state.
    """
    #: The maximum item count per block. Consensus data and Transactions are considered items.
    MAX_CONTENTS_PER_BLOCK = 65535
    #: The maximum number of transactions allowed to be included in a block.
    MAX_TX_PER_BLOCK = MAX_CONTENTS_PER_BLOCK - 1

    def __init__(self,
                 version: int = 0,
                 prev_hash: types.UInt256 = None,
                 merkle_root: types.UInt256 = None,
                 timestamp: int = 0,
                 index: int = 0,
                 next_consensus: types.UInt160 = None,
                 witness: payloads.Witness = None,
                 consensus_data: payloads.ConsensusData = None,
                 transactions: List[payloads.Transaction] = None
                 ):
        super(Block, self).__init__(version, prev_hash, merkle_root, timestamp, index, next_consensus, witness)
        self.consensus_data = consensus_data if consensus_data else payloads.ConsensusData()
        self.transactions = [] if transactions is None else transactions

    def __len__(self):
        # calculate the varint length that needs to be inserted before the transaction objects.
        magic_len = utils.get_var_size(len(self.transactions))
        txs_len = sum([len(t) for t in self.transactions])
        return super(Block, self).__len__() + magic_len + len(self.consensus_data) + txs_len

    def __eq__(self, other):
        if other is None:
            return False
        if type(self) != type(other):
            return False
        if self.hash() != other.hash():
            return False
        return True

    @property
    def inventory_type(self) -> payloads.InventoryType:
        """
        Inventory type identifier.
        """
        return payloads.InventoryType.BLOCK

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        super(Block, self).serialize(writer)
        writer.write_var_int(len(self.transactions) + 1)
        writer.write_serializable(self.consensus_data)
        for tx in self.transactions:
            writer.write_serializable(tx)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.

        Raises:
            ValueError: if the content count of the block is zero, or if there is a duplicate transaction in the list,
                or if the merkle root does not included the calculated root.
        """
        super(Block, self).deserialize(reader)
        content_count = reader.read_var_int(max=self.MAX_CONTENTS_PER_BLOCK)
        if content_count == 0:
            raise ValueError("Deserialization error - no contents")

        self.consensus_data = reader.read_serializable(payloads.ConsensusData)
        tx_count = content_count - 1
        for _ in range(tx_count):
            self.transactions.append(reader.read_serializable(payloads.Transaction))

        if len(set(self.transactions)) != tx_count:
            raise ValueError("Deserialization error - block contains duplicate transaction")

        hashes = [t.hash() for t in self.transactions]
        if Block.calculate_merkle_root(self.consensus_data.hash(), hashes) != self.merkle_root:
            raise ValueError("Deserialization error - merkle root mismatch")

    def rebuild_merkle_root(self) -> None:
        """
        Recalculates the Merkle root.
        """
        self.merkle_root = Block.calculate_merkle_root(self.consensus_data.hash(),
                                                       [t.hash() for t in self.transactions])

    def trim(self) -> TrimmedBlock:
        """
        Reduce a block in size by replacing the consensus data and transaction objects with their identifying hashes.
        """
        hashes = [self.consensus_data.hash()] + [t.hash() for t in self.transactions]
        return TrimmedBlock(version=self.version,
                            prev_hash=self.prev_hash,
                            merkle_root=self.merkle_root,
                            timestamp=self.timestamp,
                            index=self.index,
                            next_consensus=self.next_consensus,
                            witness=self.witness,
                            hashes=hashes,
                            consensus_data=self.consensus_data
                            )

    @staticmethod
    def calculate_merkle_root(consensus_data_hash: types.UInt256,
                              transaction_hashes: List[types.UInt256]) -> types.UInt256:
        """
        Calculate a Merkle root.

        Args:
            consensus_data_hash:
            transaction_hashes:
        """
        hashes = [consensus_data_hash] + transaction_hashes
        return crypto.MerkleTree.compute_root(hashes)

    def from_replica(self, replica: Block) -> None:
        self.version = replica.version
        self.prev_hash = replica.prev_hash
        self.merkle_root = replica.merkle_root
        self.timestamp = replica.timestamp
        self.index = replica.index
        self.next_consensus = replica.next_consensus
        self.witness = replica.witness
        self.consensus_data = replica.consensus_data
        self.transactions = replica.transactions


class TrimmedBlock(_BlockBase, IClonable):
    """
    A size reduced Block instance.

    Contains consensus data and transactions hashes instead of their full objects.
    """

    def __init__(self,
                 version: int = 0,
                 prev_hash: types.UInt256 = None,
                 merkle_root: types.UInt256 = None,
                 timestamp: int = 0,
                 index: int = 0,
                 next_consensus: types.UInt160 = None,
                 witness: payloads.Witness = None,
                 hashes: List[types.UInt256] = None,
                 consensus_data: payloads.ConsensusData = None):
        super(TrimmedBlock, self).__init__(version, prev_hash, merkle_root, timestamp, index, next_consensus, witness)
        self.hashes = hashes if hashes else []
        self.consensus_data = consensus_data if consensus_data else payloads.ConsensusData()

    def __len__(self):
        size = super(TrimmedBlock, self).__len__()
        size += utils.get_var_size(self.hashes)
        if self.consensus_data:
            size += len(self.consensus_data)
        return size

    def __deepcopy__(self, memodict={}):
        # not the best, but faster than letting deepcopy() do introspection
        return TrimmedBlock.deserialize_from_bytes(self.to_array())

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        super(TrimmedBlock, self).serialize(writer)
        writer.write_serializable_list(self.hashes)
        if len(self.hashes) > 0:
            writer.write_serializable(self.consensus_data)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        super(TrimmedBlock, self).deserialize(reader)
        self.hashes = reader.read_serializable_list(types.UInt256)
        if len(self.hashes) > 0:
            self.consensus_data = reader.read_serializable(payloads.ConsensusData)

    def from_replica(self, replica: TrimmedBlock) -> None:
        """
        Shallow copy attributes from a reference object.
        """
        super().from_replica(replica)
        self.version = replica.version
        self.prev_hash = replica.prev_hash
        self.merkle_root = replica.merkle_root
        self.timestamp = replica.timestamp
        self.index = replica.index
        self.next_consensus = replica.next_consensus
        self.witness = replica.witness
        self.hashes = replica.hashes
        self.consensus_data = replica.consensus_data

    def clone(self) -> TrimmedBlock:
        """
        Deep copy
        """
        return deepcopy(self)


class MerkleBlockPayload(_BlockBase):
    def __init__(self,
                 version: int = 0,
                 prev_hash: types.UInt256 = None,
                 merkle_root: types.UInt256 = None,
                 timestamp: int = 0,
                 index: int = 0,
                 next_consensus: types.UInt160 = None,
                 witness: payloads.Witness = None,
                 content_count: int = None,
                 hashes: List[types.UInt256] = None,
                 flags: bytearray = None):
        super(MerkleBlockPayload, self).__init__(version, prev_hash, merkle_root,
                                                 timestamp, index, next_consensus, witness)
        """
        Should not be called directly. Use create() instead.
        """
        self.hashes = hashes if hashes else []
        self.content_count = content_count if content_count else len(self.hashes)
        self.flags = flags if flags else b''

    def __len__(self):
        return super(MerkleBlockPayload, self).__len__() + s.uint32 + utils.get_var_size(self.hashes) + \
            utils.get_var_size(self.flags)

    @classmethod
    def create(cls, block: Block, flags: bitarray) -> MerkleBlockPayload:
        """
        Create payload.

        Should be used instead of directly calling the initializer.

        Args:
            block:
            flags:
        """
        hashes = [block.consensus_data.hash()] + [t.hash() for t in block.transactions]
        tree = crypto.MerkleTree(hashes)
        flag_bytes = flags.tobytes()

        return cls(version=block.version, prev_hash=block.prev_hash, merkle_root=block.merkle_root,
                   timestamp=block.timestamp, index=block.index, next_consensus=block.next_consensus,
                   witness=block.witness, content_count=len(hashes), hashes=tree.to_hash_array(),
                   flags=flag_bytes)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        super(MerkleBlockPayload, self).serialize(writer)
        writer.write_var_int(self.content_count)
        writer.write_serializable_list(self.hashes)
        writer.write_var_bytes(self.flags)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        super(MerkleBlockPayload, self).deserialize(reader)
        self.content_count = reader.read_var_int()
        self.hashes = reader.read_serializable_list(types.UInt256)
        self.flags = reader.read_var_bytes()


class HeadersPayload(serialization.ISerializable):
    MAX_HEADERS_COUNT = 2000

    def __init__(self, headers: List[Header] = None):
        """
        Should not be called directly. Use create() instead.
        """
        self.headers = headers if headers else []

    def __len__(self):
        return utils.get_var_size(self.headers)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_serializable_list(self.headers)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.headers = reader.read_serializable_list(Header)

    @classmethod
    def create(cls, headers: List[Header]) -> HeadersPayload:
        """
        Create payload.

        Args:
            headers: Header objects to include.
        """
        return cls(headers)


class GetBlocksPayload(serialization.ISerializable):
    """
    Used to request an array block hashes that can be retrieved via a message with the
    :const:`~neo3.network.message.MessageType.GETDATA` type.
    """

    def __init__(self, hash_start: types.UInt256 = None, count=-1):
        """
        Should not be called directly. Use create() instead.
        """
        self.hash_start = hash_start if hash_start else types.UInt256.zero()
        self.count = count

    def __len__(self):
        return s.uint256 + s.uint16

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_serializable(self.hash_start)
        writer.write_int16(self.count)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.
        """
        self.hash_start = reader.read_serializable(types.UInt256)
        self.count = reader.read_int16()

    @classmethod
    def create(cls, hash_start: types.UInt256, count=-1) -> GetBlocksPayload:
        """
        Create payload.

        Args:
            hash_start: starting point from which to return the `next` hash.

                Note:

                    For syncing supply the local best height block hash to receive the hashes in the range of
                    best_height+1 to best_height+1+count

            count: number of hashes to return.
        """
        return cls(hash_start, count)


class GetBlockDataPayload(serialization.ISerializable):
    """
    Used to request full Block objects via a message with the :const:`~neo3.network.message.MessageType.GETBLOCKDATA`
    type.
    """
    MAX_BLOCKS_COUNT = 500

    def __init__(self, index_start: int = 0, count: int = 500):
        """
        Should not be called directly. Use create() instead.
        """
        self.index_start = index_start
        self.count = count

    def __len__(self):
        return s.uint32 + s.uint16

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        """
        Serialize the object into a binary stream.

        Args:
            writer: instance.
        """
        writer.write_uint32(self.index_start)
        writer.write_uint16(self.count)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        """
        Deserialize the object from a binary stream.

        Args:
            reader: instance.

        Raises:
            ValueError: if `count` is zero or exceeds
               :const:`~neo3.network.payloads.getblocks.GetBlockDataPayload.MAX_BLOCKS_COUNT`.
        """
        self.index_start = reader.read_uint32()
        self.count = reader.read_uint16()
        if self.count == 0 or self.count > self.MAX_BLOCKS_COUNT:
            raise ValueError("Deserialization error - invalid count")

    @classmethod
    def create(cls, index_start: int, count: int = 500) -> GetBlockDataPayload:
        """
        Create payload.

        Args:
            index_start: start block height.
            count: number of blocks to requests starting from `index_start`.
        """
