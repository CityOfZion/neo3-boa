from boa3.builtin import public
from boa3.builtin.type import UInt160

@public
def uint160_method(arg: UInt160) -> bytes:
    return arg + b'123'
