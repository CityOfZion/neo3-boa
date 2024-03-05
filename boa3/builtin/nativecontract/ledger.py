__all__ = [
    'Ledger',
]

from boa3.builtin.interop.blockchain import Block, Signer, Transaction, VMState
from boa3.builtin.type import UInt256, UInt160


class Ledger:
    """
    A class used to represent the Ledger native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/Ledger>`__
    to learn more about the Ledger class.
    """

    hash: UInt160

    @classmethod
    def get_block(cls, index_or_hash: int | UInt256) -> Block | None:
        """
        Gets the block with the given index or hash.

        >>> Ledger.get_block(0)        # first block
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

        >>> Ledger.get_block(UInt256(b"S{\\xed'\\x85&\\xf5\\x93U=\\xc1\\xbf'\\x95\\xc4/\\x80X\\xdb\\xd5\\xa1-\\x97q\\x85\\xe3I\\xe5\\x99cd\\x04"))        # first block
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

        >>> Ledger.get_block(9999999)      # block doesn't exist
        None

        >>> Ledger.get_block(UInt256(bytes(32)))   # block doesn't exist
        None

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

        >>> Ledger.get_current_index()
        10908937

        >>> Ledger.get_current_index()
        2108690

        >>> Ledger.get_current_index()
        3529755

        :return: the index of the current block
        :rtype: int
        """
        pass

    @classmethod
    def get_transaction(cls, hash_: UInt256) -> Transaction | None:
        """
        Gets a transaction with the given hash.

        >>> Ledger.get_transaction(UInt256(b'\\xff\\x7f\\x18\\x99\\x8c\\x1d\\x10X{bA\\xc2\\xe3\\xdf\\xc8\\xb0\\x9f>\\xd0\\xd2G\\xe3\\xba\\xd8\\x96\\xb9\\x0e\\xc1iS\\xcdr'))
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

        >>> Ledger.get_transaction(UInt256(bytes(32)))   # transaction doesn't exist
        None

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: the Transaction, if exists. None otherwise
        """
        pass

    @classmethod
    def get_transaction_from_block(cls, block_hash_or_height: UInt256 | int, tx_index: int) -> Transaction | None:
        """
        Gets a transaction from a block.

        >>> Ledger.get_transaction_from_block(1, 0)
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

        >>> Ledger.get_transaction_from_block(UInt256(b'\\x21|\\xc2~U\\t\\x89^\\x0c\\xc0\\xd29wl\\x0b\\xad d\\xe1\\xf5U\\xd7\\xf5B\\xa5/\\x8b\\x8f\\x8b\\x22\\x24\\x80'), 0)
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

        >>> Ledger.get_transaction_from_block(123456789, 0)     # height does not exist yet
        None

        >>> Ledger.get_transaction_from_block(UInt256(bytes(32)), 0)     # block hash does not exist
        None

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

        >>> Ledger.get_transaction_height(UInt256(b'\\x28\\x89\\x4f\\xb6\\x10\\x62\\x9d\\xea\\x4c\\xcd\\x00\\x2e\\x9e\\x11\\xa6\\xd0\\x3d\\x28\\x90\\xc0\\xe5\\xd4\\xfc\\x8f\\xc6\\x4f\\xcc\\x32\\x53\\xb5\\x48\\x01'))
        2108703

        >>> Ledger.get_transaction_height(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
        10

        >>> Ledger.get_transaction_height(UInt256(bytes(32)))   # transaction doesn't exist
        -1

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: height of the transaction
        """
        pass

    @classmethod
    def get_transaction_signers(cls, hash_: UInt256) -> list[Signer]:
        """
        Gets the VM state of a transaction.

        >>> Ledger.get_transaction_signers(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
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

    @classmethod
    def get_transaction_vm_state(cls, hash_: UInt256) -> VMState:
        """
        Gets the VM state of a transaction.

        >>> Ledger.get_transaction_vm_state(UInt256(b'\\x29\\x41\\x06\\xdb\\x4c\\xf3\\x84\\xa7\\x20\\x4d\\xba\\x0a\\x04\\x03\\x72\\xb3\\x27\\x76\\xf2\\x6e\\xd3\\x87\\x49\\x88\\xd0\\x3e\\xff\\x5d\\xa9\\x93\\x8c\\xa3'))
        VMState.HALT

        :param hash_: hash identifier of the transaction
        :type hash_: UInt256
        :return: VM state of the transaction
        """
        pass
