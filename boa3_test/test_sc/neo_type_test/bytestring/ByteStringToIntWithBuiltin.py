from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def to_int(arg: ByteString) -> int:
    return ByteString.to_int(arg)
