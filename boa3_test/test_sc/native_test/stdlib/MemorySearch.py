from boa3.builtin import public
from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.type import ByteString


@public
def main(mem: ByteString, value: ByteString, start: int, backward: bool) -> int:
    return StdLib.memory_search(mem, value, start, backward)
