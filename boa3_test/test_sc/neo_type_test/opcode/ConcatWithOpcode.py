from boa3.sc.compiletime import public
from boa3.sc.types import Opcode


@public
def concat() -> Opcode:
    return Opcode.LDARG0 + Opcode.LDARG1 + Opcode.ADD
