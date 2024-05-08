from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib


@public
def main(mem: bytes | str, value: bytes | str) -> int:
    return StdLib.memory_search(mem, value)
