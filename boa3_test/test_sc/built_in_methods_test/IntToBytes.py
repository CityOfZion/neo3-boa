from boa3.sc.compiletime import public
from boa3.sc.utils import to_bytes


@public
def int_to_bytes() -> bytes:
    return to_bytes(123)
