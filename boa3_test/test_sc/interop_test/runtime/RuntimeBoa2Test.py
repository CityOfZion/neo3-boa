from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.runtime import check_witness, get_time, log, notify, trigger


@public
def main(operation: str, arg: Any) -> Any:

    if operation == 'get_trigger':
        return trigger()

    elif operation == 'check_witness' and isinstance(arg, bytes):
        return check_witness(arg)

    elif operation == 'get_time':
        return get_time

    elif operation == 'log' and isinstance(arg, str):
        log(arg)
        return True

    elif operation == 'notify':
        notify(arg)
        return True

    return 'unknown'
