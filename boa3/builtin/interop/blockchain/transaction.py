__all__ = [
    'Transaction',
]

from boa3.builtin.type import UInt160, UInt256


class Transaction:
    """
    Represents a transaction.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/foundation/Transactions>`__ to learn more about
    Transactions.

    :ivar hash: a unique identifier based on the unsigned data portion of the object
    :vartype hash: UInt256
    :ivar version: the data structure version of the transaction
    :vartype version: int
    :ivar nonce: a random number used once in the cryptography
    :vartype nonce: int
    :ivar sender: the sender is the first signer of the transaction, they will pay the fees of the transaction
    :vartype sender: UInt160
    :ivar system_fee: the fee paid for executing the `script`
    :vartype system_fee: int
    :ivar network_fee: the fee paid for the validation and inclusion of the transaction in a block by the consensus node
    :vartype network_fee: int
    :ivar valid_until_block: indicates that the transaction is only valid before this block height
    :vartype valid_until_block: int
    :ivar script: the array of instructions to be executed on the transaction chain by the virtual machine
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
