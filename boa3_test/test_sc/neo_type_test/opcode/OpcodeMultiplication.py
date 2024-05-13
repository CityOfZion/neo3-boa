from boa3.sc.compiletime import public
from boa3.sc.types import Opcode


@public
def opcode_mult(multiplier: int) -> Opcode:
    return Opcode.NOP * multiplier
