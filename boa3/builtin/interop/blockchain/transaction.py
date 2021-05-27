from boa3.builtin.type import UInt160, UInt256


class Transaction:
    """
    Represents a transaction.

    :var hash: the hash of the transaction
    :vartype hash: UInt256
    :var version: the version of the transaction
    :vartype version: int
    :var nonce: a random number used once in the cryptography
    :vartype nonce: int
    :var sender: the sender is the first signer of the transaction, they will pay the fees of the transaction
    :vartype sender: UInt160
    :var system_fee: the fee paid for network resource
    :vartype system_fee: int
    :var network_fee: the fee paid for the validator packaging transactions
    :vartype network_fee: int
    :var valid_until_block: indicates that the transaction is only valid before this block height
    :vartype valid_until_block: int
    :var script: the script of the transaction
    :vartype script: bytes
    """
    def __init__(self):
        self.hash: UInt256 = UInt256()
        self.version: int = 0
        self.nonce: int = 0
        self.sender: UInt160 = UInt160()
        self.system_fee: int = 0
        self.network_fee: int = 0
        self.valid_until_block: int = 0
        self.script: bytes = b''
