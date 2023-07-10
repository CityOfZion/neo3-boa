__all__ = [
    'GAS',
]


from typing import Any

from boa3.builtin.type import UInt160


class GAS:
    """
    A class used to represent the GAS native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/Gas>`__
    to learn more about the GAS class.
    """

    hash: UInt160

    @classmethod
    def symbol(cls) -> str:
        """
        Gets the symbol of GAS.

        >>> GAS.symbol()
        'GAS'

        :return: the GAS string.
        :rtype: str
        """
        pass

    @classmethod
    def decimals(cls) -> int:
        """
        Gets the amount of decimals used by GAS.

        >>> GAS.decimals()
        8

        :return: the number 8.
        :rtype: int
        """
        pass

    @classmethod
    def totalSupply(cls) -> int:
        """
        Gets the total token supply deployed in the system.

        >>> GAS.totalSupply()
        5199999098939320

        >>> GAS.totalSupply()
        5522957322800300

        :return: the total token supply deployed in the system.
        :rtype: int
        """
        pass

    @classmethod
    def balanceOf(cls, account: UInt160) -> int:
        """
        Get the current balance of an address.

        >>> GAS.balanceOf(UInt160(bytes(20)))
        0

        >>> GAS.balanceOf(UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'))
        1000000000

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

        >>> GAS.transfer(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'),     # this script hash needs to have signed the transaction or block
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              10000, None)
        True

        >>> GAS.transfer(UInt160(bytes(20)),
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              10000, None)
        False

        >>> GAS.transfer(UInt160(b'\\xc9F\\x17\\xba!\\x99\\x07\\xc1\\xc5\\xd6\t#\\xe1\\x9096\\x89U\\xac\\x13'),
        ...              UInt160(b'\\xabv\\xe2\\xcb\\xb0\\x16,vG\\x2f\\x44Va\\x10\\x14\\x19\\xf3\\xff\\xa1\\xe6'),
        ...              -1, None)
        False

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
