from boa3.builtin import public
from boa3.builtin.vm import Opcode


@public
def opcode_mult(multiplier: int) -> Opcode:
    return Opcode.NOP * multiplier
