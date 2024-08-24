from typing import Any

from boa3.sc.contracts import StdLib


def main(mem: bytes, value: bytes, start: int, backward: bool, arg: Any) -> int:
    return StdLib.memory_search(mem, value, start, backward, arg)
