from boa3.sc.contracts import StdLib


def main(mem1: bytes) -> int:
    return StdLib.memory_compare(mem1)
