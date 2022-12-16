from boa3.builtin.compile_time import public
from boa3.builtin.type import ByteString


@public
def to_bool(arg: ByteString) -> bool:
    return arg.to_bool()
