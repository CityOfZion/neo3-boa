from typing import List, Union

from boa3.builtin.interop.blockchain import Block, Signer, Transaction, VMState
from boa3.builtin.type import UInt256, UInt160


class Ledger:
    """
    A class used to represent the Ledger native contract
    """

    hash: UInt160

    @classmethod
    def get_block(cls, index_or_hash: Union[int, UInt256]) -> Block:
        """
        Gets the block with the given index or hash.

        :param index_or_hash: index or hash identifier of the block
        :type index_or_hash: int or UInt256
        :return: the desired block, if exists. None otherwise
        :rtype: Block or None
        """
        pass

    @classmethod
    def get_current_index(cls) -> int:
        """
        Gets the index of the current block.

        :return: the index of the current block
        :rtype: int
        """
        pass

    @classmethod
    def get_transaction(cls, hash_: UInt256) -> Transaction:
        """
        Gets a transaction with the given hash.

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: the Transaction, if exists. None otherwise
        """
        pass

    @classmethod
    def get_transaction_from_block(cls, block_hash_or_height: Union[UInt256, int], tx_index: int) -> Transaction:
        """
        Gets a transaction from a block.

        :param block_hash_or_height: a block identifier
        :type block_hash_or_height: UInt256 or int
        :param tx_index: the transaction identifier in the block
        :type tx_index: int
        :return: the Transaction, if exists. None otherwise
        """
        pass

    @classmethod
    def get_transaction_height(cls, hash_: UInt256) -> int:
        """
        Gets the height of a transaction.

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: height of the transaction
        """
        pass

    @classmethod
    def get_transaction_signers(cls, hash_: UInt256) -> List[Signer]:
        """
        Gets the VM state of a transaction.

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: VM state of the transaction
        """
        pass

    @classmethod
    def get_transaction_vm_state(cls, hash_: UInt256) -> VMState:
        """
        Gets the VM state of a transaction.

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: VM state of the transaction
        """
        pass
