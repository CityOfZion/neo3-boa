from typing import Any

from boa3.sc.contracts import StdLib


def main(mem1: bytes, mem2: bytes, arg: Any) -> int:
    return StdLib.memory_compare(mem1, mem2, arg)
