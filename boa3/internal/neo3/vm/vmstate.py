"""
    Place holder until the VM package gets fully implemented.
"""
from __future__ import annotations

from enum import IntEnum


class VMState(IntEnum):
    NONE = 0
    HALT = 1
    FAULT = 2
    BREAK = 4


def get_vm_state(state_name: str) -> VMState:
    try:
        return VMState[state_name]
    except BaseException:
        return VMState.NONE
