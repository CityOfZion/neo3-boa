__all__ = [
    'NEO',
]


from typing import Any

from boa3.builtin.contract import NeoAccountState
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.type import ECPoint, UInt160


class NEO:
    """
    A class used to represent the NEO native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/Neo>`__
    to learn more about the NEO class.
    """

    hash: UInt160

    @classmethod
    def symbol(cls) -> str:
        """
        Gets the symbol of NEO.

        >>> NEO.symbol()
        'NEO'

        :return: the NEO string.
        :rtype: str
        """
        pass

    @classmethod
    def decimals(cls) -> int:
        """
        Gets the amount of decimals used by NEO.

        >>> NEO.decimals()
        0

        :return: the number 0.
        :rtype: int
        """
        pass

    @classmethod
    def totalSupply(cls) -> int:
        """
        Gets the total token supply deployed in the system.

        >>> NEO.totalSupply()
        100000000

        :return: the total token supply deployed in the system.
        :rtype: int
        """
        pass

    @classmethod
    def balanceOf(cls, account: UInt160) -> int:
        """
        Get the current balance of an address.

        >>> NEO.balanceOf(UInt160(bytes(20)))
        0

        >>> NEO.balanceOf(UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'))
        100

        :param account: the account's address to retrieve the balance for
        :type account: UInt160
        :return: the account's balance
        :rtype: int
        """
        pass

    @classmethod
    def transfer(cls, from_address: UInt160, to_address: UInt160, amount: int, data: Any = None) -> bool:
        """
        Transfers an amount of GAS from one account to another.

        If the method succeeds, it will fire the `Transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

        >>> NEO.transfer(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'),     # this script hash needs to have signed the transaction or block
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              10, None)
        True

        >>> NEO.transfer(UInt160(bytes(20)),
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              10, None)
        False

        >>> NEO.transfer(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'),
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              -1, None)
        False


        :param from_address: the address to transfer from
        :type from_address: UInt160
        :param to_address: the address to transfer to
        :type to_address: UInt160
        :param amount: the amount of NEO to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onNEP17Payment method
        :type data: Any

        :return: whether the transfer was successful
        :rtype: bool
        :raise Exception: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
        """
        pass

    @classmethod
    def get_gas_per_block(cls) -> int:
        """
        Gets the amount of GAS generated in each block.

        >>> NEO.get_gas_per_block()
        500000000

        :return: the amount of GAS generated
        :rtype: int
        """
        pass

    @classmethod
    def unclaimed_gas(cls, account: UInt160, end: int) -> int:
        """
        Gets the amount of unclaimed GAS in the specified account.

        >>> NEO.unclaimed_gas(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'), 0)
        100000000

        >>> NEO.unclaimed_gas(UInt160(bytes(20), 0)
        100000000

        :param account: the account to check
        :type account: UInt160
        :param end: the block index used when calculating GAS
        :type end: int
        """
        pass

    @classmethod
    def register_candidate(cls, pubkey: ECPoint) -> bool:
        """
        Registers as a candidate.

        >>> NEO.register_candidate(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
        False

        :param pubkey: The public key of the account to be registered
        :type pubkey: ECPoint
        :return: whether the registration was a success or not
        :rtype: bool
        """
        pass

    @classmethod
    def unregister_candidate(cls, pubkey: ECPoint) -> bool:
        """
        Unregisters as a candidate.

        >>> NEO.unregister_candidate(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
        False

        :param pubkey: The public key of the account to be unregistered
        :type pubkey: ECPoint
        :return: whether the unregistration was a success or not
        :rtype: bool
        """
        pass

    @classmethod
    def vote(cls, account: UInt160, vote_to: ECPoint) -> bool:
        """
        Votes for a candidate.

        >>> NEO.vote(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'), ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
        False

        :param account: the account that is voting
        :type account: UInt160
        :param vote_to: the public key of the one being voted
        :type vote_to: ECPoint
        """
        pass

    @classmethod
    def get_all_candidates(cls) -> Iterator:
        """
        Gets the registered candidates iterator.

        >>> NEO.get_all_candidates()
        []

        :return: all registered candidates
        :rtype: Iterator
        """
        pass

    @classmethod
    def un_vote(cls, account: UInt160) -> bool:
        """
        Removes the vote of the candidate voted. It would be the same as calling vote(account, None).

        >>> NEO.un_vote(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'))
        False

        :param account: the account that is removing the vote
        :type account: UInt160
        """
        pass

    @classmethod
    def get_candidates(cls) -> list[tuple[ECPoint, int]]:
        """
        Gets the list of all registered candidates.

        >>> NEO.get_candidates()
        []

        :return: all registered candidates
        :rtype: list[tuple[ECPoint, int]]
        """
        pass

    @classmethod
    def get_candidate_vote(cls, pubkey: ECPoint) -> int:
        """
        Gets votes from specific candidate.

        >>> NEO.get_candidate_vote(ECPoint(b'\\x03\\x5a\\x92\\x8f\\x20\\x16\\x39\\x20\\x4e\\x06\\xb4\\x36\\x8b\\x1a\\x93\\x36\\x54\\x62\\xa8\\xeb\\xbf\\xf0\\xb8\\x81\\x81\\x51\\xb7\\x4f\\xaa\\xb3\\xa2\\xb6\\x1a'))
        100

        >>> NEO.get_candidate_vote(ECPoint(bytes(32)))
        -1

        :return: Votes or -1 if it was not found.
        :rtype: int
        """
        pass

    @classmethod
    def get_committee(cls) -> list[ECPoint]:
        """
        Gets all committee members list.

        >>> NEO.get_committee()
        [ b'\\x02|\\x84\\xb0V\\xc2j{$XG\\x1em\\xcfgR\\xed\\xd9k\\x96\\x88}x34\\xe3Q\\xdd\\xfe\\x13\\xc4\\xbc\\xa2' ]

        :return: all committee members
        :rtype: list[ECPoint]
        """
        pass

    @classmethod
    def get_next_block_validators(cls) -> list[ECPoint]:
        """
        Gets validators list of the next block.

        >>> NEO.get_next_block_validators()
        [ b'\\x02|\\x84\\xb0V\\xc2j{$XG\\x1em\\xcfgR\\xed\\xd9k\\x96\\x88}x34\\xe3Q\\xdd\\xfe\\x13\\xc4\\xbc\\xa2' ]

        :return: the public keys of the validators
        :rtype: list[ECPoint]
        """
        pass

    @classmethod
    def get_account_state(cls, account: UInt160) -> NeoAccountState:
        """
        Gets the latest votes of the specified account.

        >>> NEO.get_account_state(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'))
        {
            'balance': 100,
            'height': 2,
            'vote_to': None,
        }

        :param account: the specified account
        :type account: UInt160
        :return: the state of the account
        :rtype: NeoAccountState
        """
        pass
