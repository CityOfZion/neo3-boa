from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem1: bytes) -> int:
    return StdLib.memory_compare(mem1)
