from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def to_str(arg: ByteString) -> str:
    return ByteString.to_str(arg)
