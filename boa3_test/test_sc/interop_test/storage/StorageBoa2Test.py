from typing import Any

from boa3.builtin import public
from boa3.builtin.interop.storage import put, delete, get


@public
def main(operation: str, arg: str, val: str) -> Any:

    print("context")

    if operation == 'sget':

        return get(arg)

    elif operation == 'sput':

        put(arg, val)
        return True

    elif operation == 'sdel':

        delete(arg)
        return True

    return 'unknown operation'
