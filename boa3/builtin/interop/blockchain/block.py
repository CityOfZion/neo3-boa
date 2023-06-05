__all__ = [
    'Block'
]

from boa3.builtin.type import UInt160, UInt256


class Block:
    """
    Represents a block.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Blocks>`__ to learn more
    about Blocks.

    :ivar hash: a unique identifier based on the unsigned data portion of the object
    :vartype hash: UInt256
    :ivar version: the data structure version of the block
    :vartype version: int
    :ivar previous_hash: the hash of the previous block
    :vartype previous_hash: UInt256
    :ivar merkle_root: the merkle root of the transactions
    :vartype merkle_root: UInt256
    :ivar timestamp: UTC timestamp of the block in milliseconds
    :vartype timestamp: int
    :ivar nonce: a random number used once in the cryptography
    :vartype nonce: int
    :ivar index: the index of the block
    :vartype index: int
    :ivar primary_index: the primary index of the consensus node that generated this block
    :vartype primary_index: int
    :ivar next_consensus: the script hash of the consensus nodes that generates the next block
    :vartype next_consensus: UInt160
    :ivar transaction_count: the number of transactions on this block
    :vartype transaction_count: int
    """

    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.previous_hash: UInt256 = UInt256()
        self.merkle_root: UInt256 = UInt256()
        self.timestamp: int = 0
        self.nonce: int = 0
        self.index: int = 0
        self.primary_index: int = 0
        self.next_consensus: UInt160 = UInt160()
        self.transaction_count: int = 0
