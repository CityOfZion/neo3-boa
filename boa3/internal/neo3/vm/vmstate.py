from enum import IntEnum


class VMState(IntEnum):
    """
    Represents the VM execution state.
    """
    NONE = 0
    """
    Indicates that the execution is in progress or has not yet begun.

    :meta hide-value:
    """

    HALT = 1
    """
    Indicates that the execution has been completed successfully.

    :meta hide-value:
    """

    FAULT = 2
    """
    Indicates that the execution has ended, and an exception that cannot be caught is thrown.

    :meta hide-value:
    """

    BREAK = 4
    """
    Indicates that a breakpoint is currently being hit.

    :meta hide-value:
    """

    def __str__(self) -> str:
        return self.name


def get_vm_state(state_name: str) -> VMState:
    try:
        return VMState[state_name]
    except BaseException:
        return VMState.NONE
