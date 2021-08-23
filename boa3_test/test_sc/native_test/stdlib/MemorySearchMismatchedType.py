from boa3.builtin.nativecontract.stdlib import StdLib


def main() -> int:
    return StdLib.memory_search(1, 1, 1, 1)
