from boa3.builtin.type import UInt160, UInt256


class Block:
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
