from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.storage import delete, get, get_context, put_str


@public
def main(operation: str, arg: bytes, val: str) -> Any:

    storage_context = get_context()
    print("context")

    if operation == 'sget':

        return get(arg, storage_context)

    elif operation == 'sput':

        put_str(arg, val, storage_context)
        return True

    elif operation == 'sdel':

        delete(arg, storage_context)
        return True

    return 'unknown operation'
