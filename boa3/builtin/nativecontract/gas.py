from typing import Any

from boa3.builtin.type import UInt160


class GAS:
    """
    A class used to represent the GAS native contract
    """

    @classmethod
    def symbol(cls) -> str:
        """
        Gets the symbol of GAS.

        :return: the GAS string.
        :rtype: str
        """
        pass

    @classmethod
    def decimals(cls) -> int:
        """
        Gets the amount of decimals used by GAS.

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
        :param amount: the amount of GAS to transfer
        :type amount: int
        :param data: whatever data is pertinent to the onNEP17Payment method
        :type data: Any

        :return: whether the transfer was successful
        :rtype: bool
        :raise Exception: raised if `from_address` or `to_address` length is not 20 or if `amount` is less than zero.
        """
        pass
