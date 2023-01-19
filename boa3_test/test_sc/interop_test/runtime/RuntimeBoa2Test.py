from typing import Any

from boa3.builtin import type
from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import check_witness, get_trigger, log, notify, time


@public
def main(operation: str, arg: Any) -> Any:

    if operation == 'get_trigger':
        return get_trigger()

    elif operation == 'check_witness' and isinstance(arg, (type.UInt160, type.ECPoint)):
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
