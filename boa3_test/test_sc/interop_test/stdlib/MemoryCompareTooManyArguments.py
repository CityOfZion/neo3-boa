from typing import Any

from boa3.builtin.interop.stdlib import memory_compare


def main(mem1: bytes, mem2: bytes, arg: Any) -> int:
    return memory_compare(mem1, mem2, arg)
