__all__ = [
    'get_exec_fee_factor',
    'get_fee_per_byte',
    'get_storage_price',
    'is_blocked',
]


from boa3.builtin.type import UInt160


def get_exec_fee_factor() -> int:
    """
    Gets the execution fee factor. This is a multiplier that can be adjusted by the committee to adjust the system fees
    for transactions.

    >>> get_exec_fee_factor()
    30

    :return: the execution fee factor
    :rtype: int
    """
    pass


def get_fee_per_byte() -> int:
    """
    Gets the network fee per transaction byte.

    >>> get_fee_per_byte()
    1000

    :return: the network fee per transaction byte
    :rtype: int
    """
    pass


def get_storage_price() -> int:
    """
    Gets the storage price.

    >>> get_storage_price()
    100000

    :return: the snapshot used to read data
    :rtype: int
    """
    pass


def is_blocked(account: UInt160) -> bool:
    """
    Determines whether the specified account is blocked.

    >>> is_blocked(UInt160(b'\\xcfv\\xe2\\x8b\\xd0\\x06,JG\\x8e\\xe3Ua\\x01\\x13\\x19\\xf3\\xcf\\xa4\\xd2'))
    False

    :param account: the account to be checked
    :type account: UInt160

    :return: whether the account is blocked or not
    :rtype: bool
    """
    pass
