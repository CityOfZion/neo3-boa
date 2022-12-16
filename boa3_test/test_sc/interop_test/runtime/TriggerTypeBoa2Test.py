from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import TriggerType, get_trigger


@public
def main(arg: int) -> Any:

    if arg == 1:
        return TriggerType.APPLICATION

    elif arg == 2:
        return TriggerType.VERIFICATION

    elif arg == 3:

        if get_trigger() == TriggerType.APPLICATION:
            return b'\x20'

    return -1
