from typing import Union

from boa3.builtin.interop.blockchain.block import Block
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160, UInt256

current_height: int = 0


def get_contract(hash: UInt160) -> Contract:
    """
    Gets a contract with a given hash

    :param hash: a smart contract hash
    :type hash: UInt160
    :return: a contract
    :rtype: Contract
    :raise Exception: raised if hash length isn't 20 bytes
    """
    pass


def get_block(index_or_hash: Union[int, UInt256]) -> Block:
    """
    Gets the block with the given index or hash

    :param index_or_hash: index or hash identifier of the block
    :type index_or_hash: int or UInt256
    :return: the desired block, if exists. None otherwise
    :rtype: Block or None
    """
    pass
