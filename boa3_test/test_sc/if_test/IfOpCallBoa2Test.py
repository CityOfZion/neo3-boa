from typing import Any

from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import hash160, sha256


@public
def main(operation: str, a: Any, b: Any) -> Any:

    if operation == 'omin' and isinstance(a, int) and isinstance(b, int):
        return min(a, b)

    elif operation == 'omax' and isinstance(a, int) and isinstance(b, int):
        return max(a, b)

    elif operation == 'sha256':
        return sha256(a)

    elif operation == 'hash160':
        return hash160(a)

    return 'unknown'
