from boa3.builtin import public
from boa3.builtin.interop.binary import serialize


@public
def serialize_dict() -> bytes:
    return serialize({1: 1, 2: 1, 3: 2})
