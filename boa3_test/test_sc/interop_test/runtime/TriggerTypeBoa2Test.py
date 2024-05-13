from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.runtime import get_trigger
from boa3.sc.types import TriggerType


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
