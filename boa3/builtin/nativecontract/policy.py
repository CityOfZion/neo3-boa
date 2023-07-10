__all__ = [
    'Policy',
]


from boa3.builtin.type import UInt160


class Policy:
    """
    A class used to represent the Policy native contract.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/native/Policy>`__
    to learn more about the Policy class.
    """

    hash: UInt160

    @classmethod
    def get_fee_per_byte(cls) -> int:
        """
        Gets the network fee per transaction byte.

        >>> Policy.get_fee_per_byte()
        1000

        :return: the network fee per transaction byte
        :rtype: int
        """
        pass

    @classmethod
    def get_exec_fee_factor(cls) -> int:
        """
        Gets the execution fee factor. This is a multiplier that can be adjusted by the committee to adjust the system fees
        for transactions.

        >>> Policy.get_exec_fee_factor()
        30

        :return: the execution fee factor
        :rtype: int
        """
        pass

    @classmethod
    def get_storage_price(cls) -> int:
        """
        Gets the storage price.

        >>> Policy.get_storage_price()
        100000

        :return: the snapshot used to read data
        :rtype: int
        """
        pass

    @classmethod
    def is_blocked(cls, account: UInt160) -> bool:
        """
        Determines whether the specified account is blocked.

        >>> Policy.is_blocked(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))
        False

        :param account: the account to be checked
        :type account: UInt160

        :return: whether the account is blocked or not
        :rtype: bool
        """
        pass
