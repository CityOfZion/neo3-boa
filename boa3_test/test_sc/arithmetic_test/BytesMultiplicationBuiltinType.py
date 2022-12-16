from boa3.builtin.compile_time import public
from boa3.builtin.interop.storage.findoptions import FindOptions


@public
def bytes_mult(a: bytes, b: FindOptions) -> bytes:
    return a * b
