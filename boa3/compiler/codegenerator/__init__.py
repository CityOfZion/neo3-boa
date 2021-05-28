from typing import List, Tuple

from boa3.neo.vm.opcode.Opcode import Opcode


def get_bytes_count(instructions: List[Tuple[Opcode, bytes]]) -> int:
    return sum([len(opcode) + len(arg) for opcode, arg in instructions])
