from enum import IntFlag


class TriggerType(IntFlag):
    """
    Represents the triggers for running smart contracts. Triggers enable the contract to execute different logic under
    different usage scenarios.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/services/TriggerType>`__
    to learn more about TriggerTypes.
    """

    ON_PERSIST = 0x01
    """
    Indicate that the contract is triggered by the system to execute the OnPersist method of the native contracts.

    :meta hide-value:
    """

    POST_PERSIST = 0x02
    """
    Indicate that the contract is triggered by the system to execute the PostPersist method of the native contracts.

    :meta hide-value:
    """

    SYSTEM = ON_PERSIST | POST_PERSIST
    """
    The combination of all system triggers.

    :meta hide-value:
    """

    VERIFICATION = 0x20
    """
    Indicates that the contract is triggered by the verification of a IVerifiable.

    :meta hide-value:
    """

    APPLICATION = 0x40
    """
    Indicates that the contract is triggered by the execution of transactions.

    :meta hide-value:
    """

    ALL = ON_PERSIST | POST_PERSIST | VERIFICATION | APPLICATION
    """
    The combination of all triggers.

    :meta hide-value:
    """


class CallFlags(IntFlag):
    """
    Defines special behaviors allowed when invoking smart contracts, e.g., chain calls, sending notifications and
    modifying states.

    Check out `Neo's Documentation <https://developers.neo.org/docs/n3/reference/scapi/framework/services/CallFlags>`__
    to learn more about CallFlags.
    """

    NONE = 0
    """
    Special behaviors of the invoked contract are not allowed, such as chain calls, sending notifications, modifying 
    state, etc.

    :meta hide-value:
    """

    READ_STATES = 0b00000001
    """
    Indicates that the called contract is allowed to read states.

    :meta hide-value:
    """

    WRITE_STATES = 0b00000010
    """
    Indicates that the called contract is allowed to write states.

    :meta hide-value:
    """

    ALLOW_CALL = 0b00000100
    """
    Indicates that the called contract is allowed to call another contract.

    :meta hide-value:
    """

    ALLOW_NOTIFY = 0b00001000
    """
    Indicates that the called contract is allowed to send notifications.

    :meta hide-value:
    """

    STATES = READ_STATES | WRITE_STATES
    """
    Indicates that the called contract is allowed to read or write states.

    :meta hide-value:
    """

    READ_ONLY = READ_STATES | ALLOW_CALL
    """
    Indicates that the called contract is allowed to read states or call another contract.

    :meta hide-value:
    """

    ALL = STATES | ALLOW_CALL | ALLOW_NOTIFY
    """
    All behaviors of the invoked contract are allowed.

    :meta hide-value:
    """
