from boa3.builtin.type import UInt160, UInt256


class Transaction:
    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.nonce: int = 0
        self.sender: UInt160 = UInt160()
        self.system_fee: int = 0
        self.network_fee: int = 0
        self.valid_until_block: int = 0
        self.script: bytes = b''
