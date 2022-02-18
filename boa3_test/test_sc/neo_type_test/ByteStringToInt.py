from boa3.builtin import public
from boa3.builtin.type import ByteString


@public
def to_int(arg: ByteString) -> int:
    return arg.to_int()
