from typing import Any

from boa3.sc.compiletime import public
from boa3.sc.contracts import CryptoLib
from boa3.sc.utils import hash160


@public
def main(operation: str, a: Any, b: Any) -> Any:

    if operation == 'omin' and isinstance(a, int) and isinstance(b, int):
        return min(a, b)

    elif operation == 'omax' and isinstance(a, int) and isinstance(b, int):
        return max(a, b)

    elif operation == 'sha256' and isinstance(a, bytes):
        return CryptoLib.sha256(a)

    elif operation == 'hash160' and isinstance(a, bytes):
        return hash160(a)

    return 'unknown'
