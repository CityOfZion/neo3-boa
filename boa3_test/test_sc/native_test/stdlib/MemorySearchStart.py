from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(mem: bytes | str, value: bytes | str, start: int) -> int:
    return StdLib.memory_search(mem, value, start)
