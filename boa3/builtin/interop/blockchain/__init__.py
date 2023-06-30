__all__ = [
    'Block',
    'Signer',
    'Transaction',
    'VMState',
    'get_contract',
    'get_block',
    'get_transaction',
    'get_transaction_from_block',
    'get_transaction_height',
    'get_transaction_signers',
    'get_transaction_vm_state',
    'current_hash',
    'current_index',
]

from typing import List, Optional, Union

from boa3.builtin.interop.blockchain.block import Block
from boa3.builtin.interop.blockchain.signer import Signer
from boa3.builtin.interop.blockchain.transaction import Transaction
from boa3.builtin.interop.blockchain.vmstate import VMState
from boa3.builtin.interop.contract import Contract
from boa3.builtin.type import UInt160, UInt256


def get_contract(hash: UInt160) -> Optional[Contract]:
    """
    Gets a contract with a given hash. If the script hash is not associated with a smart contract, then it will return
    None.

    >>> get_contract(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))    # GAS script hash
    {
        'id': -6,
        'update_counter': 0,
        'hash': b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2',
        'nef': b'NEF3neo-core-v3.0\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00#\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@\\x10A\\x1a\\xf7{g@QA\\xc7\\x9e',
        'manifest': {
            'name': 'GasToken',
            'group': [],
            'supported_standards': ['NEP-17'],
            'abi': [[['balanceOf', [['account', 20]], 17, 0, True], ['decimals', [], 17, 7, True], ['symbol', [], 19, 14, True], ['totalSupply', [], 17, 21, True], ['transfer', [['from', 20], ['to', 20], ['amount', 17], ['data', 0]], 16, 28, False]], [['Transfer', [['from', 20], ['to', 20], ['amount', 17]]]]],
            'permissions': [[None, None]],
            'trusts': [],
            'extras': 'null'
        },
    }

    >>> get_contract(UInt160(bytes(20)))    # there is no smart contract associated with this script hash
    None

    :param hash: a smart contract hash
    :type hash: UInt160
    :return: a contract
    :rtype: Contract

    :raise Exception: raised if hash length isn't 20 bytes.
    """
    pass


def get_block(index_or_hash: Union[int, UInt256]) -> Optional[Block]:
    """
    Gets the block with the given index or hash. Will return None if the index or hash is not associated with a Block.

    >>> get_block(0)        # first block
    {
        'hash': b"S{\\xed'\\x85&\\xf5\\x93U=\\xc1\\xbf'\\x95\\xc4/\\x80X\\xdb\\xd5\\xa1-\\x97q\\x85\\xe3I\\xe5\\x99cd\\x04",
        'version': 0,
        'previous_hash': '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        'merkle_root': '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        'timestamp': 1468595301000,
        'nonce': 2083236893,
        'index': 0,
        'primary_index': 0,
        'next_consensus': b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
        'transaction_count': 0,
    }

    >>> get_block(UInt256(b"S{\\xed'\\x85&\\xf5\\x93U=\\xc1\\xbf'\\x95\\xc4/\\x80X\\xdb\\xd5\\xa1-\\x97q\\x85\\xe3I\\xe5\\x99cd\\x04"))        # first block
    {
        'hash': b"S{\\xed'\\x85&\\xf5\\x93U=\\xc1\\xbf'\\x95\\xc4/\\x80X\\xdb\\xd5\\xa1-\\x97q\\x85\\xe3I\\xe5\\x99cd\\x04",
        'version': 0,
        'previous_hash': '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        'merkle_root': '\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00',
        'timestamp': 1468595301000,
        'nonce': 2083236893,
        'index': 0,
        'primary_index': 0,
        'next_consensus': b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
        'transaction_count': 0,
    }

    >>> get_block(9999999)      # block doesn't exist
    None

    >>> get_block(UInt256(bytes(32)))   # block doesn't exist
    None

    :param index_or_hash: index or hash identifier of the block
    :type index_or_hash: int or UInt256
    :return: the desired block, if exists. None otherwise
    :rtype: Block or None
    """
    pass


def get_transaction(hash_: UInt256) -> Optional[Transaction]:
    """
    Gets a transaction with the given hash. Will return None if the hash is not associated with a Transaction.

    >>> get_transaction(UInt256(b'\\xff\\x7f\\x18\\x99\\x8c\\x1d\\x10X{bA\\xc2\\xe3\\xdf\\xc8\\xb0\\x9f>\\xd0\\xd2G\\xe3\\xba\\xd8\\x96\\xb9\\x0e\\xc1iS\\xcdr'))
    {
        'hash': b'\\xff\\x7f\\x18\\x99\\x8c\\x1d\\x10X{bA\\xc2\\xe3\\xdf\\xc8\\xb0\\x9f>\\xd0\\xd2G\\xe3\\xba\\xd8\\x96\\xb9\\x0e\\xc1iS\\xcdr',
        'version': 0,
        'nonce': 2025056010,
        'sender': b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
        'system_fee': 2028330,
        'network_fee': 1206580,
        'valid_until_block': 5761,
        'script': b'\\x0c\\x14\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04\\x11\\xc0\\x1f\\x0c\\tbalanceOf\\x0c\\x14\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2Ab}[R',
    }

    >>> get_transaction(UInt256(bytes(32)))   # transaction doesn't exist
    None

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: the Transaction, if exists. None otherwise
    """
    pass


def get_transaction_from_block(block_hash_or_height: Union[UInt256, int], tx_index: int) -> Optional[Transaction]:
    """
    Gets a transaction from a block. Will return None if the block hash or height is not associated with a Transaction.

    >>> get_transaction_from_block(1, 0)
    {
        'hash': b'\\xff\\x7f\\x18\\x99\\x8c\\x1d\\x10X{bA\\xc2\\xe3\\xdf\\xc8\\xb0\\x9f>\\xd0\\xd2G\\xe3\\xba\\xd8\\x96\\xb9\\x0e\\xc1iS\\xcdr',
        'version': 0,
        'nonce': 2025056010,
        'sender': b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
        'system_fee': 2028330,
        'network_fee': 1206580,
        'valid_until_block': 5761,
        'script': b'\\x0c\\x14\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04\\x11\\xc0\\x1f\\x0c\\tbalanceOf\\x0c\\x14\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2Ab}[R',
    }

    >>> get_transaction_from_block(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'), 0)
    {
        'hash': b'\\xff\\x7f\\x18\\x99\\x8c\\x1d\\x10X{bA\\xc2\\xe3\\xdf\\xc8\\xb0\\x9f>\\xd0\\xd2G\\xe3\\xba\\xd8\\x96\\xb9\\x0e\\xc1iS\\xcdr',
        'version': 0,
        'nonce': 2025056010,
        'sender': b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
        'system_fee': 2028330,
        'network_fee': 1206580,
        'valid_until_block': 5761,
        'script': b'\\x0c\\x14\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04\\x11\\xc0\\x1f\\x0c\\tbalanceOf\\x0c\\x14\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2Ab}[R',
    }

    >>> get_transaction_from_block(123456789, 0)     # height does not exist yet
    None

    >>> get_transaction_from_block(UInt256(bytes(32)), 0)     # block hash does not exist
    None

    :param block_hash_or_height: a block identifier
    :type block_hash_or_height: UInt256 or int
    :param tx_index: the transaction identifier in the block
    :type tx_index: int
    :return: the Transaction, if exists. None otherwise
    """
    pass


def get_transaction_height(hash_: UInt256) -> int:
    """
    Gets the height of a transaction. Will return -1 if the hash is not associated with a Transaction.

    >>> get_transaction_height(UInt256(b'\\x28\\x89\\x4f\\xb6\\x10\\x62\\x9d\\xea\\x4c\\xcd\\x00\\x2e\\x9e\\x11\\xa6\\xd0\\x3d\\x28\\x90\\xc0\\xe5\\xd4\\xfc\\x8f\\xc6\\x4f\\xcc\\x32\\x53\\xb5\\x48\\x01'))
    2108703

    >>> get_transaction_height(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
    10

    >>> get_transaction_height(UInt256(bytes(32)))   # transaction doesn't exist
    -1

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: height of the transaction
    """
    pass


def get_transaction_signers(hash_: UInt256) -> List[Signer]:
    """
    Gets a list with the signers of a transaction.

    >>> get_transaction_signers(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
    [
        {
            "account": b'\\xa6\\xea\\xb0\\xae\\xaf\\xb4\\x96\\xa1\\x1b\\xb0|\\x88\\x17\\xcar\\xa5J\\x00\\x12\\x04',
            "scopes": 1,
            "allowed_contracts": [],
            "allowed_groups": [],
            "rules": [],
        },
    ]

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: VM state of the transaction
    """
    pass


def get_transaction_vm_state(hash_: UInt256) -> VMState:
    """
    Gets the VM state of a transaction.

    >>> get_transaction_vm_state(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
    VMState.HALT

    :param hash_: hash identifier of the transaction
    :type hash_: UInt256
    :return: VM state of the transaction
    """
    pass


current_hash: UInt256 = UInt256()
"""
Gets the hash of the current block.

>>> current_hash
b'\\x3e\\x65\\xe5\\x4d\\x75\\x5a\\x94\\x90\\xd6\\x98\\x3a\\x77\\xe4\\x82\\xaf\\x7a\\x38\\xc9\\x8c\\x1a\\xc6\\xd9\\xda\\x48\\xbd\\x7c\\x22\\xb3\\x2a\\x9e\\x34\\xea'

:meta hide-value:
"""

current_index: int = 0
"""
Gets the index of the current block.

>>> current_index
10908937

>>> current_index
2108690

>>> current_index
3529755

:meta hide-value:
"""
