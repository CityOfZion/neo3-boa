from boa3.builtin import public
from boa3.builtin.type import ByteString


@public
def concat(arg: ByteString) -> str:
    return '12345' + arg
