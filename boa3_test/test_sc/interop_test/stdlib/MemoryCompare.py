from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(mem1: str | bytes, mem2: str | bytes) -> int:
    return StdLib.memory_compare(mem1, mem2)
