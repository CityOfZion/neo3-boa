from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def to_bytes(arg: ByteString) -> bytes:
    return arg.to_bytes()
