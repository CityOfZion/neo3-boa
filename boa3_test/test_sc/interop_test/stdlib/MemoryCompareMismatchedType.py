from boa3.sc.contracts import StdLib


def main() -> int:
    return StdLib.memory_compare(1, 1)
