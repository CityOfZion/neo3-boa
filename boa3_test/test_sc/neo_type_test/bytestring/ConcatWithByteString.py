from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def concat(arg1: ByteString, arg2: ByteString) -> ByteString:
    return arg1 + arg2