from boa3.builtin.type import UInt160


def get_exec_fee_factor() -> int:
    """
    Gets the execution fee factor. This is a multiplier that can be adjusted by the committee to adjust the system fees
    for transactions.

    :return: the execution fee factor
    :rtype: int
    """
    pass


def get_fee_per_byte() -> int:
    """
    Gets the network fee per transaction byte.

    :return: the network fee per transaction byte
    :rtype: int
    """
    pass


def get_storage_price() -> int:
    """
    Gets the storage price.

    :return: the snapshot used to read data
    :rtype: int
    """
    pass


def is_blocked(account: UInt160) -> bool:
    """
    Determines whether the specified account is blocked.

    :param account: the account to be checked
    :type account: UInt160

    :return: whether the account is blocked or not
    :rtype: bool
    """
    pass
