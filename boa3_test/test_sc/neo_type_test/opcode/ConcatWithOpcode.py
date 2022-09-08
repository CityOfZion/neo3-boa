from boa3.builtin import public
from boa3.builtin.vm import Opcode


@public
def concat() -> Opcode:
    return Opcode.LDARG0 + Opcode.LDARG1 + Opcode.ADD
