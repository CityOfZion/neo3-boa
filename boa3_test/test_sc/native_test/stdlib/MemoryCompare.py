from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.type import ByteString


@public
def main(mem1: ByteString, mem2: ByteString) -> int:
    return StdLib.memory_compare(mem1, mem2)
