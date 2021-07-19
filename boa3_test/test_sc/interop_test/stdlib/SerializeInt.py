from boa3.builtin import public
from boa3.builtin.interop.stdlib import serialize


@public
def serialize_int() -> bytes:
    return serialize(42)
