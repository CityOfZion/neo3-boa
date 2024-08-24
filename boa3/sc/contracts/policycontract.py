__all__ = [
    'PolicyContract',
]

from boa3.internal.neo3.network.payloads.transactionattributetype import TransactionAttributeType
from boa3.sc.types import UInt160


class PolicyContract:
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

        >>> PolicyContract.get_fee_per_byte()
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

        >>> PolicyContract.get_exec_fee_factor()
        30

        :return: the execution fee factor
        :rtype: int
        """
        pass

    @classmethod
    def get_storage_price(cls) -> int:
        """
        Gets the storage price.

        >>> PolicyContract.get_storage_price()
        100000

        :return: the storage price
        :rtype: int
        """
        pass

    @classmethod
    def get_attribute_fee(cls, attribute_type: TransactionAttributeType) -> int:
        """
        Gets the fee for attribute.

        >>> PolicyContract.get_attribute_fee(TransactionAttributeType.HIGH_PRIORITY)
        0

        :return: the fee for attribute
        :rtype: int
        """
        pass

    @classmethod
    def is_blocked(cls, account: UInt160) -> bool:
        """
        Determines whether the specified account is blocked.

        >>> PolicyContract.is_blocked(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))
        False

        :param account: the account to be checked
        :type account: boa3.sc.types.UInt160

        :return: whether the account is blocked or not
        :rtype: bool
        """
        pass

    @classmethod
    def set_attribute_fee(cls, attribute_type: TransactionAttributeType, value: int) -> None:
        """
        Sets the fee for attribute. You need to sign the transaction using a committee member, otherwise, this function
        will throw an error.

        >>> PolicyContract.set_attribute_fee(TransactionAttributeType.HIGH_PRIORITY, 10)
        None
        """
        pass
