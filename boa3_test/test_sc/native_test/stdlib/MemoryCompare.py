from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(mem1: bytes | str, mem2: bytes | str) -> int:
    return StdLib.memory_compare(mem1, mem2)
