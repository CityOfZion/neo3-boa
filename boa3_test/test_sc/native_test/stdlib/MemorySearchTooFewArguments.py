from boa3.sc.contracts import StdLib


def main(mem: bytes) -> int:
    return StdLib.memory_search(mem)
