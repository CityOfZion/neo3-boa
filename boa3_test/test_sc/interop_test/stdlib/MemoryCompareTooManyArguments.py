from typing import Any

from boa3.builtin.interop.stdlib import memory_compare
from boa3.builtin.type import ByteString


def main(mem1: ByteString, mem2: ByteString, arg: Any) -> int:
    return memory_compare(mem1, mem2, arg)
