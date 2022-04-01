from boa3.builtin import public
from boa3.builtin.type import ByteString


@public
def concat(arg: ByteString) -> bytes:
    return b'12345' + arg
