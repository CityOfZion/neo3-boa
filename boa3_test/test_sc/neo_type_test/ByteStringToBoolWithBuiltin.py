from boa3.builtin import public
from boa3.builtin.type import ByteString


@public
def to_bool(arg: ByteString) -> bool:
    return ByteString.to_bool(arg)
