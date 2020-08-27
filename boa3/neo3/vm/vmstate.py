"""
    Place holder until the VM package gets fully implemented.
"""
from enum import IntEnum


class VMState(IntEnum):
    NONE = 0
    HALT = 1
    FAULT = 2
    BREAK = 4
