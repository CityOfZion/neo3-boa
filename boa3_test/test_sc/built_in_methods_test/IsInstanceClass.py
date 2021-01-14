from boa3.builtin import public
from boa3.builtin.type import UInt160


@public
def Main(value: bytes) -> bool:
    if len(value) == 20:
        value = UInt160(value)

    # not supported because boa builtin classes don't work with isinstance yet
    return isinstance(value, UInt160)
