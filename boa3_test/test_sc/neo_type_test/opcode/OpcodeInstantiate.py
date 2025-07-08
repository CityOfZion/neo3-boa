from boa3.sc.compiletime import public
from boa3.sc.types import Opcode


@public
def main(opcode: bytes) -> Opcode:
    return Opcode(opcode)
