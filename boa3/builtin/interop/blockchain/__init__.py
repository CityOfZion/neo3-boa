from typing import List, Union

from boa3.builtin.interop.blockchain.block import Block
from boa3.builtin.interop.blockchain.signer import Signer
from boa3.builtin.interop.blockchain.transaction import Transaction
from boa3.builtin.interop.blockchain.vmstate import VMState
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160, UInt256


def get_contract(hash: UInt160) -> Contract:
    """
    Gets a contract with a given hash.

    :param hash: a smart contract hash
    :type hash: UInt160
    :return: a contract
    :rtype: Contract

    :raise Exception: raised if hash length isn't 20 bytes.
    """
    pass


def get_block(index_or_hash: Union[int, UInt256]) -> Block:
    """
    Gets the block with the given index or hash.

    :param index_or_hash: index or hash identifier of the block
    :type index_or_hash: int or UInt256
    :return: the desired block, if exists. None otherwise
    :rtype: Block or None
    """
    pass


def get_transaction(hash_: UInt256) -> Transaction:
    """
    Gets a transaction with the given hash.

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: the Transaction, if exists. None otherwise
    """
    pass


def get_transaction_from_block(block_hash_or_height: Union[UInt256, int], tx_index: int) -> Transaction:
    """
    Gets a transaction from a block.

    :param block_hash_or_height: a block identifier
    :type block_hash_or_height: UInt256 or int
    :param tx_index: the transaction identifier in the block
    :type tx_index: int
    :return: the Transaction, if exists. None otherwise
    """
    pass


def get_transaction_height(hash_: UInt256) -> int:
    """
    Gets the height of a transaction.

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: height of the transaction
    """
    pass


def get_transaction_signers(hash_: UInt256) -> List[Signer]:
    """
    Gets the VM state of a transaction.

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: VM state of the transaction
    """
    pass


def get_transaction_vm_state(hash_: UInt256) -> VMState:
    """
    Gets the VM state of a transaction.

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: VM state of the transaction
    """
    pass


current_hash: UInt256 = UInt256()
"""
Gets the hash of the current block.

:meta hide-value:
"""

current_index: int = 0
"""
Gets the index of the current block.

:meta hide-value:
"""
