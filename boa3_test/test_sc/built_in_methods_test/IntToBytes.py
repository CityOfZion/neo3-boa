from boa3.builtin.compile_time import public
from boa3.builtin.type.helper import to_bytes


@public
def int_to_bytes() -> bytes:
    return to_bytes(123)
