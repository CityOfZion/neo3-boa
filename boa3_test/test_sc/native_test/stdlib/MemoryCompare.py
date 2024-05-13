from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(mem1: bytes | str, mem2: bytes | str) -> int:
    return StdLib.memory_compare(mem1, mem2)
