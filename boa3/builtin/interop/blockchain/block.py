from boa3.builtin.type import UInt160, UInt256


class Block:
    """
    Represents a block.

    :var hash: the hash of the block
    :vartype hash: UInt256
    :var version: the version of the block
    :vartype version: int
    :var previous_hash: the hash of the previous block
    :vartype previous_hash: UInt256
    :var merkle_root: the merkle root of the transactions
    :vartype merkle_root: UInt256
    :var timestamp: the timestamp of the block
    :vartype timestamp: int
    :var index: the index of the block
    :vartype index: int
    :var primary_index: the primary index of the consensus node that generated this block
    :vartype primary_index: int
    :var next_consensus: the multi-signature address of the consensus nodes that generates the next block
    :vartype next_consensus: UInt160
    :var transaction_count: the number of transactions on this block
    :vartype transaction_count: int
    """
    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.previous_hash: UInt256 = UInt256()
        self.merkle_root: UInt256 = UInt256()
        self.timestamp: int = 0
        self.index: int = 0
        self.primary_index: int = 0
        self.next_consensus: UInt160 = UInt160()
        self.transaction_count: int = 0
