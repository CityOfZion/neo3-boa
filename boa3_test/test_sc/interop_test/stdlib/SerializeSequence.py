from boa3.builtin.compile_time import public
from boa3.builtin.interop.stdlib import serialize


@public
def serialize_sequence() -> bytes:
    return serialize([2, 3, 5, 7])
