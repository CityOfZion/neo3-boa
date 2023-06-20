from boa3.builtin.nativecontract.stdlib import StdLib


def main(mem: bytes) -> int:
    return StdLib.memory_search(mem)
