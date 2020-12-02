from boa3.builtin import public
from boa3.builtin.interop.binary import serialize


@public
def serialize_sequence() -> bytes:
    return serialize([2, 3, 5, 7])
