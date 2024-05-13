from boa3.sc.compiletime import public
from boa3.sc.contracts import StdLib


@public
def main(mem: str | bytes, value: str | bytes) -> int:
    return StdLib.memory_search(mem, value)
