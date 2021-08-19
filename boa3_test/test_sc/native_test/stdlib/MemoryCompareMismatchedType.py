from boa3.builtin.nativecontract.stdlib import StdLib


def main() -> int:
    return StdLib.memory_compare(1, 1)
