from boa3.builtin.nativecontract.stdlib import StdLib
from boa3.builtin.type import ByteString


def main(mem: ByteString) -> int:
    return StdLib.memory_search(mem)
