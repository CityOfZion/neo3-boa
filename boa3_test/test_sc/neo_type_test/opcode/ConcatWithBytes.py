from boa3.builtin import public
from boa3.builtin.vm import Opcode


@public
def concat(arg: Opcode) -> bytes:
    return b'12345' + arg
