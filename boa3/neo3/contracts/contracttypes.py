from enum import IntFlag


class TriggerType(IntFlag):
    """
    Represents the triggers for running smart contracts. Triggers enable the contract to execute different logic under
    different usage scenarios.
    """

    # TODO: add ONPERSIST and POSTPERSIST
    SYSTEM = 0x01   #: The combination of all system triggers.
    VERIFICATION = 0x20  #: Indicates that the contract is triggered by the verification of a IVerifiable.
    APPLICATION = 0x40  #: Indicates that the contract is triggered by the execution of transactions.
    ALL = SYSTEM | VERIFICATION | APPLICATION  #: The combination of all triggers


class CallFlags(IntFlag):
    """
    Defines special behaviors allowed when invoking smart contracts, e.g., chain calls, sending notifications and
    modifying states.
    """

    NONE = 0  #: Special behaviors of the invoked contract are not allowed, such as chain calls, sending notifications, modifying state, etc.

    READ_STATES = 0b00000001  #: Indicates that the called contract is allowed to read states.
    WRITE_STATES = 0b00000010  #: Indicates that the called contract is allowed to write states.
    ALLOW_CALL = 0b00000100  #: Indicates that the called contract is allowed to call another contract.
    ALLOW_NOTIFY = 0b00001000  #: Indicates that the called contract is allowed to send notifications.

    STATES = READ_STATES | WRITE_STATES  #: Indicates that the called contract is allowed to read or write states.
    READ_ONLY = READ_STATES | ALLOW_CALL  #: Indicates that the called contract is allowed to read states or call another contract.
    ALL = STATES | ALLOW_CALL | ALLOW_NOTIFY  #: All behaviors of the invoked contract are allowed.
