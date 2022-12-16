from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import serialize


@public
def serialize_dict() -> bytes:
    return serialize({1: 1, 2: 1, 3: 2})
