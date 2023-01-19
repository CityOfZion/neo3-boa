from typing import Any, List, Tuple

from boa3.builtin.contract import NeoAccountState
from boa3.builtin.interop.iterator import Iterator
from boa3.builtin.type import ECPoint, UInt160


class NEO:
    """
    A class used to represent the NEO native contract
    """

    hash: UInt160

    @classmethod
    def symbol(cls) -> str:
        """
        Gets the symbol of NEO.

        :return: the NEO string.
        :rtype: str
        """
        pass

    @classmethod
    def decimals(cls) -> int:
        """
        Gets the amount of decimals used by NEO.

        :return: the number 8.
        :rtype: int
        """
        pass

    @classmethod
    def totalSupply(cls) -> int:
        """
        Gets the total token supply deployed in the system.

        :return: the total token supply deployed in the system.
        :rtype: int
        """
        pass

    @classmethod
    def balanceOf(cls, account: UInt160) -> int:
        """
        Get the current balance of an address.

        :param account: the account's address to retrieve the balance for
        :type account: UInt160
        :return: the account's balance
        :rtype: int
        """
        pass

    @classmethod
    def transfer(cls, from_address: UInt160, to_address: UInt160, amount: int, data: Any = None) -> bool:
        """
        Transfers an amount of GAS from one account to another

        If the method succeeds, it will fire the `Transfer` event and must return true, even if the amount is 0,
        or from and to are the same address.

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

        :return: the amount of GAS generated
        :rtype: int
        """
        pass

    @classmethod
    def unclaimed_gas(cls, account: UInt160, end: int) -> int:
        """
        Gets the amount of unclaimed GAS in the specified account.

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

        :return: all registered candidates
        :rtype: Iterator
        """
        pass

    @classmethod
    def un_vote(cls, account: UInt160) -> bool:
        """
        Removes the vote of the candidate voted. It would be the same as calling vote(account, None).

        :param account: the account that is removing the vote
        :type account: UInt160
        """
        pass

    @classmethod
    def get_candidates(cls) -> List[Tuple[ECPoint, int]]:
        """
        Gets the list of all registered candidates.

        :return: all registered candidates
        :rtype: List[Tuple[ECPoint, int]]
        """
        pass

    @classmethod
    def get_candidate_vote(cls, pubkey: ECPoint) -> int:
        """
        Gets votes from specific candidate.

        :return: Votes or -1 if it was not found.
        :rtype: int
        """
        pass

    @classmethod
    def get_committee(cls) -> List[ECPoint]:
        """
        Gets all committee members list.

        :return: all committee members
        :rtype: List[ECPoint]
        """
        pass

    @classmethod
    def get_next_block_validators(cls) -> List[ECPoint]:
        """
        Gets validators list of the next block.

        :return: the public keys of the validators
        :rtype: List[ECPoint]
        """
        pass

    @classmethod
    def get_account_state(cls, account: UInt160) -> NeoAccountState:
        """
        Gets the latest votes of the specified account.

        :param account: the specified account
        :type account: UInt160
        :return: the state of the account
        :rtype: NeoAccountState
        """
        pass
