from boa3.builtin import public
from boa3.builtin.interop.binary import serialize


@public
def serialize_bool() -> bytes:
    return serialize(True)
