from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.runtime import check_witness, get_trigger, log, notify, time
from boa3.sc.types import UInt160, ECPoint


@public
def main(operation: str, arg: Any) -> Any:

    if operation == 'get_trigger':
        return get_trigger()

    elif operation == 'check_witness' and isinstance(arg, (UInt160, ECPoint)):
        return check_witness(arg)

    elif operation == 'time':
        return time

    elif operation == 'log' and isinstance(arg, str):
        log(arg)
        return True

    elif operation == 'notify':
        notify(arg)
        return True

    return 'unknown'
