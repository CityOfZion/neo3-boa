from boa3.sc.compiletime import public
from boa3.sc.types import Opcode


@public
def concat(arg: Opcode) -> bytes:
    return b'12345' + arg
