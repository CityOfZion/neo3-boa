from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage import delete, get, get_context, put


@public
def main(operation: str, arg: bytes, val: str) -> Any:

    storage_context = get_context()
    print("context")

    if operation == 'sget':

        return get(arg, storage_context)

    elif operation == 'sput':

        put(arg, val, storage_context)
        return True

    elif operation == 'sdel':

        delete(arg, storage_context)
        return True

    return 'unknown operation'
