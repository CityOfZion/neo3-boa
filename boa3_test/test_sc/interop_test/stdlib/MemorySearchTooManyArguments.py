from typing import Any

from boa3.builtin.interop.stdlib import memory_search


def main(mem: bytes, value: bytes, start: int, backward: bool, arg: Any) -> int:
    return memory_search(mem, value, start, backward, arg)
