from boa3.builtin.compile_time import public
from boa3.builtin.type import UInt160


@public
def Main(value: bytes) -> bool:
    if len(value) == 20:
        value = UInt160(value)

    return isinstance(value, UInt160)
