from enum import IntEnum


class TransactionAttributeType(IntEnum):
    """
    Represents the TransactionAttributeType for running smart contracts.
    """

    HIGH_PRIORITY = 0x01
    """
    Indicates that the transaction is of high priority.
    
    :meta hide-value:
    """

    ORACLE_RESPONSE = 0x11
    """
    Indicates that the transaction is an oracle response

    :meta hide-value:
    """

    NOT_VALID_BEFORE = 0x20
    """
    Indicates that the transaction is not valid before height.

    :meta hide-value:
    """

    CONFLICTS = 0x21
    """
    Indicates that the transaction conflicts with hash.

    :meta hide-value:
    """
